window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                classes,
                colorScale,
                expectedWages,
                style
            } = context.hideout;
            for (let countyIndex = 0; countyIndex < expectedWages.length; countyIndex++) {
                for (let i = 0; i < classes.length; i++) {
                    if (expectedWages[countyIndex][0].includes(feature.properties.name)) {
                        if (expectedWages[countyIndex][expectedWages.length - 1] > classes[i]) {
                            style.fillColor = colorScale[i];
                        }
                    }
                }
            }
            return style;
        }
    }
});