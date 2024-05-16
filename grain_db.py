"""
File: grain_db.py

Description: Extracts grains from audio files, and records the frames and an analysis
"""

import os
import sqlite3
import audiopython.audiofile as audiofile
import audiopython.granulator as granulator
import audiopython.sampler as sampler
import audiopython.analysis as analysis
import audiopython.basic_operations as basic_operations
import numpy as np
import random


def analyze_grains(grains):
    """
    Analyzes grains and prepares for storage in the database
    :param grains: The grains to analyze
    :return: The analysis of the grains
    """
    analyses = []
    for grain in grains:
        a = audiofile.read(grain[1])
        g = granulator.extract_grain(np.reshape(a.samples, (a.samples.size)), grain[2], grain[3] - grain[2], max_window_size=512)
        ax = analysis.analyzer(g, a.sample_rate)
        analyses.append((
            grain[0],
            ax["dbfs"],
            ax["energy"],
            ax["pitch"],
            ax["midi"],
            ax["spectral_centroid"],
            ax["spectral_entropy"],
            ax["spectral_flatness"],
            ax["spectral_slope"][0],
            ax["spectral_slope"][1],
            ax["spectral_variance"],
            ax["spectral_skewness"],
            ax["spectral_kurtosis"],
            ax["spectral_roll_off_0.5"],
            ax["spectral_roll_off_0.75"],
            ax["spectral_roll_off_0.9"],
            ax["spectral_roll_off_0.95"],
            ax["zero_crossing_rate"],
            ))
    return analyses


def connect_to_db(path, schema_path):
    """
    Connects to a SQLite database and populates the tables if necessary

    :param path: The path to the SQLite database
    :param schema_path: The path to the SQL schema file if the database does not exist
    :return: Returns the database connection and a cursor for SQL script execution
    
    NOTE: You will need to manually close the database connection that is returned from this function!
    """
    if os.path.exists(path):
        db = sqlite3.connect(path)
        cursor = db.cursor()
    else:
        db = sqlite3.connect(path)
        cursor = db.cursor()
        with open(schema_path, 'r') as schema:
            schema_text = schema.read()
            cursor.executescript(schema_text)
            db.commit()
    return db, cursor


def extract_random_grains(directory, n, size, dbfs_floor, instrument_family):
    """
    Extracts grains from all samples in a given directory
    :param directory: The directory with the samples
    :param n: The number of grains to extract
    :param size: The size in frames of each grain
    :param dbfs_floor: The lowest peak dBFS allowed for a grain
    :param instrument_family: The instrument family name
    :return: A list of grains
    """
    grains = []
    MAX_JUMP = size + 2048  # The maximum number of frames to jump forward randomly
    MIN_JUMP = 512  # The minimum number of frames to jump forward randomly

    # Load samples
    samples = sampler.load_samples(directory)
    print(f"Extracting grains from {directory}...")
    for sample in samples:
        sample.instrument_family = instrument_family
        sample.instrument_name = sample.instrument_name.lower()
        i = 0
        start_pos = 0
        print(f"file: {os.path.split(sample.path)[-1]}: ", end="")

        # Try to extract n grains, but we cannot extract beyond the end of the sample.
        # We extract grains moving from the beginning to the end of the file.
        while i < n and start_pos + size < sample.frames:
            frame1 = start_pos + random.randrange(MIN_JUMP, MAX_JUMP)
            frame2 = frame1 + size
            start_pos = frame1
            if frame2 < sample.frames:
                # The grain we extracted
                grain = sample.samples[frame1:frame2]
                dbfs = basic_operations.dbfs_max_local(grain, 1, 1)

                # If the grain is valid
                if dbfs >= dbfs_floor:
                    i += 1
                    grains.append((
                        sample.path,
                        frame1,
                        frame2,
                        sample.sample_rate,
                        (frame2 - frame1) / sample.sample_rate,
                        basic_operations.midicps(sample.midi),
                        sample.midi,
                        sample.dynamic_name,
                        sample.instrument_name,
                        sample.instrument_family,
                        sample.string_name
                    ))
        print(f"{i} grains extracted")
    
    return grains
    

def retrieve_grains(db, cursor, analyzed=None):
    """
    Retrieves grains from the database
    :param db: A connection to a SQLite database
    :param cursor: The cursor for executing SQL
    :param analyzed: Whether to retrieve only grains that have been analyzed or have not been analyzed. 
    If None, will retrive all grains. If True, will retrieve only analyzed grains. 
    If False, will retrieve only unanalyzed grains.
    :return: The grains
    """
    if analyzed is None:
        SQL = """
            SELECT *
            FROM grains;
            """
    elif analyzed == True:
        SQL = """
            SELECT grains.*
            FROM grains
            LEFT JOIN analysis ON grains.id = analysis.grain_id;
            """
    else:
        SQL = """
            SELECT grains.*
            FROM grains
            LEFT JOIN analysis ON grains.id = analysis.grain_id 
            WHERE analysis.grain_id IS NULL;
            """
    return cursor.execute(SQL)


def store_analyses(analyses, db, cursor):
    """
    Stores analyses in the database
    :param analyses: A list of grain analyses
    :param db: A connection to a SQLite database
    :param cursor: The cursor for executing SQL
    """
    SQL = "INSERT INTO analysis VALUES(NULL, " + "?, " * 17 + "?)"
    cursor.executemany(SQL, analyses)
    db.commit()


def store_grains(grains, db, cursor):
    """
    Stores grains in the database
    :param grains: A list of grain dictionaries
    :param db: A connection to a SQLite database
    :param cursor: The cursor for executing SQL
    """
    SQL = "INSERT INTO grains VALUES(NULL, " + "?, " * 10 + "?)"
    cursor.executemany(SQL, grains)
    db.commit()


if __name__ == "__main__":
    random.seed()
    DB_FILE = "grains.sqlite3"
    DB_SCHEMA = "schema.sql"
    db, cursor = connect_to_db(DB_FILE, DB_SCHEMA)
    SAMPLE_DIR = "D:\\Recording\\Samples\\Iowa\\Viola.arco.mono.2444.1\\samples"
    # grains = extract_random_grains(SAMPLE_DIR, 5, 8192, -30, "string")
    # store_grains(grains, db, cursor)
    a = retrieve_grains(db, cursor, False)
    ax = analyze_grains(a)
    store_analyses(ax, db, cursor)
    db.close()
