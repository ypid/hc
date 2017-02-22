#!/usr/bin/env bats

teardown() {
    rm -f ./integration-test-output/schulferien_de_SH_2017-2019_copy.*
}

@test "Integration testing schulferien_html" {
    rm -f ./integration-test-output/schulferien_de_SH_2017-2019*
    for format in yaml json; do
        hc -c ./cache/ -F '2017-01' -T '2019-12' -f schulferien_html -t "${format}" "./integration-test-output/schulferien_de_SH_2017-2019.${format}"
        cp "./integration-test-output/schulferien_de_SH_2017-2019.${format}" "./integration-test-output/schulferien_de_SH_2017-2019_copy.${format}"
        hc -c ./cache/ -F '2017-01' -T '2019-12' -f schulferien_html -t "${format}" --update-output "./integration-test-output/schulferien_de_SH_2017-2019_copy.${format}"
        diff "./integration-test-output/schulferien_de_SH_2017-2019.${format}" "./integration-test-output/schulferien_de_SH_2017-2019_copy.${format}"
    done
    git diff --exit-code -- ./integration-test-output
}

@test "Integration testing schulferien_html with testing data" {
    rm -f ./integration-test-output/opening_hours.js_de*
    if command -v yaml2json >/dev/null
    then
        yaml2json --pretty ./integration-test-input/opening_hours.js_de.yaml > ./integration-test-input/opening_hours.js_de.json
    fi
    cp ./integration-test-input/opening_hours.js_de.* ./integration-test-output/
    for format in yaml json; do
        hc -c ./cache/ -F '2017-01' -T '2017-02' -f schulferien_html -t "${format}" --update-output "./integration-test-output/opening_hours.js_de.${format}"
    done
    git diff --exit-code -- ./integration-test-output
}
