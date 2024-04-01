CC := g++
CPPFLAGS := -std=c++11
OPENCV_LIBS := `pkg-config opencv4 --cflags --libs`

all: aruco_reader

aruco_reader: main.cpp
	$(CC) $(CPPFLAGS) $< -o $@ $(OPENCV_LIBS)

clean:
	rm -f aruco_reader
