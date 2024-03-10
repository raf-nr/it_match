cmake_minimum_required(VERSION 3.23)
project(first_task C)

set(CMAKE_C_STANDARD 99)

# Указываем путь к заголовочным файлам OpenMP
find_path(OPENMP_INCLUDE_DIR omp.h HINTS /opt/homebrew/opt/libomp/include)

# Указываем путь к библиотекам OpenMP
find_library(OPENMP_LIB libomp.dylib HINTS /opt/homebrew/opt/libomp/lib)

if(OPENMP_INCLUDE_DIR AND OPENMP_LIB)
    # Добавляем флаги OpenMP для компилятора
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Xpreprocessor -fopenmp")
    # Добавляем путь к заголовочным файлам OpenMP
    include_directories(${OPENMP_INCLUDE_DIR})
    # Создаем исполняемый файл
    add_executable(first_task main1.c)
    # Указываем, что нужно линковаться с OpenMP
    target_link_libraries(first_task PUBLIC ${OPENMP_LIB})
else()
    message(FATAL_ERROR "OpenMP не найден. Пожалуйста, убедитесь, что OpenMP установлен и пути к заголовочным файлам и библиотекам указаны правильно.")
endif()