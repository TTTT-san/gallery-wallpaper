#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#define MAX_PATH_LENGTH 260 // Lunghezza massima per i percorsi in Windows

void setWallpaper(const char *imagePath) {
    if (SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, (PVOID) imagePath, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)) {
        //printf("Sfondo cambiato con successo a %s\n", imagePath);
    } else {
        //printf("Errore nel cambiare lo sfondo a %s\n", imagePath);
    }
}

// Funzione di confronto per qsort
int compareStrings(const void *a, const void *b) {
    return strcmp(*(const char **) a, *(const char **) b);
}

// Funzione per trovare i file immagine
int findImageFiles(const char *folderPath, char ***imageFiles, int *fileCount) {
    WIN32_FIND_DATA findFileData;
    HANDLE hFind;
    char searchPath[MAX_PATH_LENGTH];
    const char *extensions[] = {"*.jpeg", "*.jpg", "*.png", "*.bmp", "*.gif"};
    const int numExtensions = sizeof(extensions) / sizeof(extensions[0]);
    int count = 0;
    int capacity = 10; // Capacità iniziale dell'array

    *imageFiles = malloc(capacity * sizeof(char *));
    if (*imageFiles == NULL) {
        perror("malloc");
        return -1;
    }

    for (int i = 0; i < numExtensions; ++i) {
        snprintf(searchPath, MAX_PATH_LENGTH, "%s\\%s", folderPath, extensions[i]);
        hFind = FindFirstFile(searchPath, &findFileData);

        if (hFind == INVALID_HANDLE_VALUE) {
            continue;
        }

        do {
            if (!(findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
                if (count >= capacity) {
                    capacity *= 2;
                    *imageFiles = realloc(*imageFiles, capacity * sizeof(char *));
                    if (*imageFiles == NULL) {
                        perror("realloc");
                        FindClose(hFind);
                        return -1;
                    }
                }
                // Allocazione dinamica solo per il percorso del file
                (*imageFiles)[count] = malloc(MAX_PATH_LENGTH * sizeof(char));
                if ((*imageFiles)[count] == NULL) {
                    perror("malloc");
                    FindClose(hFind);
                    return -1;
                }
                snprintf((*imageFiles)[count], MAX_PATH_LENGTH, "%s\\%s", folderPath, findFileData.cFileName);
                count++;
            }
        } while (FindNextFile(hFind, &findFileData) != 0);

        FindClose(hFind);
    }

    *fileCount = count;

    // Ordina i file trovati
    qsort(*imageFiles, *fileCount, sizeof(char *), compareStrings);

    return 0;
}

void cycleWallpapers(char **imageFiles, int fileCount) {
    int index = 0;
    printf("Impostando sfondo: %s\n", imageFiles[1]);
    int sleepTimer = 5000;
    while (1) {
        // Aggiunta stampa per mostrare il percorso dell'immagine

        // Cambia lo sfondo
        setWallpaper(imageFiles[index]);
        Sleep(sleepTimer);
        // Passa al prossimo file
        index = (index + 1) % fileCount;
    }
}

int main() {
    char folderPath[MAX_PATH_LENGTH] = "I:\\Other computers\\My Laptop\\Project\\Python\\gallery-wallpaper\\change-background\\images";
    char **imageFiles;
    int fileCount;

    // Trova tutti i file immagine nella cartella
    if (findImageFiles(folderPath, &imageFiles, &fileCount) != 0) {
        printf("Errore nel trovare i file immagine.\n");
        return 1;
    }

    if (fileCount == 0) {
        printf("Nessun file immagine trovato nella cartella %s\n", folderPath);
        return 1;
    }

    // Avvia il ciclo infinito per cambiare gli sfondi desktop
    cycleWallpapers(imageFiles, fileCount);

    // Qui non c'è la liberazione della memoria, come richiesto
    // I percorsi delle immagini non vengono liberati, ma restano in memoria

    return 0;
}
