__author__ = 'missoni'

"""
Compiles list of features to files.
"""

from features import AccelerationFeature
from features import AngleFeature
import numpy as np
from utils import get_trip_npy, list_all_drivers
from utils import PATHTODRIVERDATA


def compile_features(features):
    """
    for each feature, do:
      for each driver, do:
        for each trip, do:
          create numpy file: driver_id, trip_id, feature_value

    :param features: list of features, each a derivative of Feature type.
    :param trips: list of trips, for each driver
    """
    def compile_feature(feature, fname):
        """
        Compiles a feature to file.

        - compute value for each driver and trip
        - store result to file
        """
        drivers = list_all_drivers(PATHTODRIVERDATA)
        trips = range(1, 201)

        values = np.empty((len(drivers)*len(trips), 3))

        for driver_index, driver in enumerate(drivers):
            print 'starting driver', driver_index
            for trip_index, trip in enumerate(trips):
                trip_points = get_trip_npy(driver, trip, PATHTODRIVERDATA)

                value = feature.compute(trip_points)
                values[driver_index*len(trips)+trip_index:] = np.array((driver, trip, value))

        with open(fname, 'w') as f:
            np.save(f, values)

        with open(fname) as f:
            assert np.load(f).all() == values.all(), "File not written correctly"

    for index, feature in enumerate(features):
        print 'computing', str(feature)
        compile_feature(feature, '../features_npy/feat%d.npy' % index)


if __name__ == '__main__':
    # select features for pre-compilation
    features = [AccelerationFeature(10, 31, True, np.median),
                AccelerationFeature(30, 51, True, np.median),
                AccelerationFeature(30, 51, False, np.median),
                AccelerationFeature(50, 71, True, np.median),
                AccelerationFeature(50, 71, False, np.median),
                AngleFeature(0, np.mean), ]

    compile_features(features)