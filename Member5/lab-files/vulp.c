/* Educational adaptation of SEED Labs' vulp.c (Wenliang Du).
 * See ../README.md for source and CC BY-NC-SA 4.0 attribution.
 * Build flags select separate slow and least-privilege experiments.
 */
#define _DEFAULT_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#ifndef DEMO_DELAY
#define DEMO_DELAY 0
#endif

int main(void)
{
    const char *fn = "/tmp/XYZ";
    char buffer[60];
    FILE *fp;
#ifdef LEAST_PRIVILEGE
    uid_t privileged_euid = geteuid();
#endif

    if (scanf("%50s", buffer) != 1) {
        fprintf(stderr, "No input received\n");
        return 1;
    }

#ifdef LEAST_PRIVILEGE
    /* Drop BEFORE both the check and the open. Saved UID permits restoration. */
    if (seteuid(getuid()) == -1) {
        perror("seteuid: drop");
        return 1;
    }
#endif

    if (access(fn, W_OK) != 0) {
        puts("No permission");
        return 1;
    }

#if DEMO_DELAY > 0
    printf("Check passed; RUID=%lu EUID=%lu; waiting %d seconds...\n",
           (unsigned long)getuid(), (unsigned long)geteuid(), DEMO_DELAY);
    fflush(stdout);
    sleep(DEMO_DELAY);
#endif

    /* Deliberate TOCTOU: pathname is resolved again, after the access check. */
    fp = fopen(fn, "a+");
    if (fp == NULL) {
        perror("Open failed");
        return 1;
    }
    int write_failed = (fwrite("\n", 1, 1, fp) != 1);
    if (fwrite(buffer, 1, strlen(buffer), fp) != strlen(buffer))
        write_failed = 1;
    if (fclose(fp) != 0)
        write_failed = 1;
    if (write_failed) {
        fprintf(stderr, "Write or close failed\n");
        return 1;
    }

#ifdef LEAST_PRIVILEGE
    /* File work is finished. This lab demonstrates temporary privilege drop.
     * A real app should not restore privilege if no later operation needs it. */
    if (seteuid(privileged_euid) == -1) {
        perror("seteuid: restore");
        return 1;
    }
#endif
    return 0;
}
