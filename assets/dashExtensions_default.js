window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                classes,
                colorScale,
                expectedWages,
                style,
                year
            } = context.hideout;
            for (let countyIndex = 0; countyIndex < expectedWages.length; countyIndex++) {
                console.log(year);
                for (let i = 0; i < classes.length; i++) {
                    if (expectedWages[countyIndex][0].includes(feature.properties.EER13NM)) {
                        if (expectedWages[countyIndex][1][year] < classes[i]) {
                            style.fillColor = colorScale[i];
                            break;
                        }
                    }
                }
            }
            return style;
        }
    }
});