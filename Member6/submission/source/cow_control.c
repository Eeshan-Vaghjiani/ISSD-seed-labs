/* Normal COW control: a writable PRIVATE mapping of a read-only-opened file
 * changes this process's copy, not the underlying /zzz file. No racing. */
#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main(void)
{
    struct stat st;
    int fd = open("/zzz", O_RDONLY);
    if (fd == -1 || fstat(fd, &st) == -1) {
        perror("open/fstat /zzz");
        return 1;
    }
    if (st.st_size <= 0 || st.st_size > 4096) {
        fputs("Reset the small dummy file first.\n", stderr);
        return 1;
    }
    size_t length = (size_t)st.st_size;
    char *map = mmap(NULL, length, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);
    if (map == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    char *where = memmem(map, length, "222222", 6);
    if (where == NULL) {
        fputs("Original pattern absent. Reset /zzz.\n", stderr);
        return 1;
    }
    memcpy(where, "******", 6);
    printf("Private memory: %.*s\n", (int)length, map);
    char original[4096];
    ssize_t count = pread(fd, original, length, 0);
    if (count != (ssize_t)length) {
        fputs("Could not read complete backing file.\n", stderr);
        return 1;
    }
    printf("Backing file:   %.*s\n", (int)length, original);
    munmap(map, length);
    close(fd);
    return 0;
}
