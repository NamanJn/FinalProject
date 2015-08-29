

import video_validation

complex_vids_dirS = 'complex_collision_vids'
complex_annotation = video_validation.InspectVideos(complex_vids_dirS, 'what type is it?', ["1","2","3"])
complex_annotation.inspectVideos(complex_vids_dirS, 'tube4', 'type_annotated', regex=r"collision(\d+)")
