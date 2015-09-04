
import configurations
import video_validation
from os.path import join

def annotateVideos():

    complex_vids_dirS = 'complex_collision_vids'

    complex_annotation = video_validation.InspectVideos(complex_vids_dirS, 'what type is it?',
                                                        ["1", "2", "3"], regex=r"collision(\d+)")

    complex_annotation.output_file_pathS = 'output/tube4/validation_results/type_annotated.csv'
    complex_annotation.inspectVideos(complex_vids_dirS, 'tube4', 'type_annotated.csv', repeat_validation=False)
    #complex_annotation.getRemainingVideosToValidate()

def trainAnnotatedVideos(user_dir):
    pass


if __name__ == "__main__":
    user_dir = 'tube4'
    results_dir_path = join(configurations.output_dir, user_dir)
    features_file_path = join(results_dir_path)
