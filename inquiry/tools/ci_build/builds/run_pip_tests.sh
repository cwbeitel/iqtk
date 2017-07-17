# BAZEL_FLAGS="--test_lang_filters=py \
#	  --build_tests_only -k --test_tag_filters=${PIP_TEST_FILTER_TAG} \
#	    --test_timeout 300,450,1200,3600"

# BAZEL_TEST_TARGETS="//inquiry/..."

# Actually run the tests.
# bazel test ${BAZEL_FLAGS} -- ${BAZEL_TEST_TARGETS}
