#ifndef SEGMENTATION_H
#define SEGMENTATION_H

#include <list>
#include <QPoint>

typedef struct
{
    int vals[2];
}PixelPosition;

typedef struct
{
    int vals[3];
}PixelColor;

class SeedManager
{
public:
    SeedManager();
    ~SeedManager();

    void clear();
    void addSeed(int x, int y);
    bool hasSeed(int x, int y);

    std::list<PixelPosition> * mpSeeds;
};

class Segmentation
{
public:
    Segmentation(const char* filename, SeedManager * foreground, SeedManager * background);
    ~Segmentation();

    void visualize();
    void process();

    std::list<PixelPosition> mForegroundSet;
    std::list<PixelPosition> mBackgroundSet;
    char * mpFilename;
};

#endif // SEGMENTATION_H