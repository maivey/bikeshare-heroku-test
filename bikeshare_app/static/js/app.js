var filter = d3.select('#mainFilter').text().slice(14,30).trim();
var city = d3.select('#mainCity').text().slice(12,30).trim();
var month = d3.select('#mainMonth').text().slice(13,30).trim();
var day = d3.select('#mainDay').text().slice(11,30).trim();
// console.log(filter)
// console.log(city)
// console.log(month)
// console.log(day)
var CITY_DATA = { 'chicago': '/outputData/chicago_filtered.csv',
'new york city': '/outputData/nyc_filtered.csv',
'washington': '/outputData/washington_filtered.csv' }
// console.log(CITY_DATA)
var myCity = CITY_DATA[city];
// console.log(cityPath)

d3.csv(myCity).then((data) => {
    // ==================================
    // ==================================
    // --- FREQUENT TIMES OF TRAVEL: ---

    if (filter === 'Day') {
        // ==================================
        // MOST COMMON MONTHS (TRACE 1)
        var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June"]
        var months = data.map(x => new Date(x['Start Time']).getMonth())
        var month_counts = []
        // var jan_count = months.filter(x => x === 0).length
        for (var i=0;i<=5;i++) {
            var month_count = months.filter(x => x === i).length
            month_counts.push(month_count)
        };
        var trace1 = {
            x : month_names,
            y : month_counts,
            // text : month_counts,
            text : month_counts.map(x => 'Trip Count : ' + x),
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layout1 = {
            title : {text: '<b>Trip Count per Month</b>'},
            xaxis : { title : {text: 'Month'} },
            yaxis : { title : {text: 'Number of Trips'} }
            };
        var data1 = [trace1];
        Plotly.newPlot('bar_month', data1, layout1);
        // console.log(month_counts)
    }  //Ends if filter=day or none
    else if (filter === 'Month') {
        // ==================================
        // MOST COMMON DAYS (TRACE 2)
        var weekday = new Array(7);
        weekday[0] = "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";

        var day_counts = []
        var days = data.map(x => weekday[new Date(x['Start Time']).getDay()])
        for (var i=0;i<=weekday.length;i++) {
            var day_count = days.filter(x => x===weekday[i]).length
            day_counts.push(day_count)
        };
        console.log(day_counts)
        var trace2 = {
            x : weekday,
            y : day_counts,
            text: day_counts.map(x => 'Trip Count : ' + x),
            // text : day_counts,
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layout2 = {
            title : {text: '<b>Trip Count per Day of the Week</b>'},
            xaxis : { title : {text: 'Day of the Week'} },
            yaxis : { title : {text: 'Number of Trips'} }
            };
        var data2 = [trace2];
        Plotly.newPlot('bar_day', data2, layout2);
        // var sun = days.filter(x => x===weekday[2]).length
        // console.log(sun)
        // console.log(days)
    } //Ends if filter=month or none
    else if (filter === 'None') {
        // ==================================
        // MOST COMMON MONTHS (TRACE 1)
        var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June"]
        var months = data.map(x => new Date(x['Start Time']).getMonth())
        var month_counts = []
        // var jan_count = months.filter(x => x === 0).length
        for (var i=0;i<=5;i++) {
            var month_count = months.filter(x => x === i).length
            month_counts.push(month_count)
        };
        var trace1 = {
            x : month_names,
            y : month_counts,
            // text : month_counts,
            text : month_counts.map(x => 'Trip Count : ' + x),
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layout1 = {
            title : {text: '<b>Trip Count per Month</b>'},
            xaxis : { title : {text: 'Month'} },
            yaxis : { title : {text: 'Number of Trips'} }
            };
        var data1 = [trace1];
        Plotly.newPlot('bar_month', data1, layout1);
        // ==================================
        // MOST COMMON DAYS (TRACE 2)
        var weekday = new Array(7);
        weekday[0] = "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";

        var day_counts = []
        var days = data.map(x => weekday[new Date(x['Start Time']).getDay()])
        for (var i=0;i<=weekday.length;i++) {
            var day_count = days.filter(x => x===weekday[i]).length
            day_counts.push(day_count)
        };
        console.log(day_counts)
        var trace2 = {
            x : weekday,
            y : day_counts,
            text: day_counts.map(x => 'Trip Count : ' + x),
            // text : day_counts,
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layout2 = {
            title : {text: '<b>Trip Count per Day of the Week</b>'},
            xaxis : { title : {text: 'Day of the Week'} },
            yaxis : { title : {text: 'Number of Trips'} }
            };
        var data2 = [trace2];
        Plotly.newPlot('bar_day', data2, layout2);
    }; // Ends if filter=none


    
    
    // ==================================
    // MOST COMMON HOURS (TRACE 3)
    var hours = data.map(x => new Date(x['Start Time']).getHours())
    var uniqueHours = []
    var hour_counts = []
    // console.log(hours)
    for (var i=0;i<=24;i++) {
    var hour_count = hours.filter(x => x===i).length
    uniqueHours.push(i)
    hour_counts.push(hour_count)
    };
    // console.log(hour_counts)

    var amPM = ['12am']
    for (var i=1;i<=24;i++) {
    if (i < 12) {
        var hour_am = i.toString() + 'am'
        amPM.push(hour_am)
    }
    else if (i == 12) {
        var hour_pm = '12pm'
        amPM.push(hour_pm)
    }
    else if (i>12) {
        var hour_pm = (i-12).toString() + 'pm'
        amPM.push(hour_pm)
    }
    };
    var trace3 = {
    x : uniqueHours,
    y : hour_counts,
    text : hour_counts.map(x => 'Trip Count : ' + x),
    type : 'bar',
    transforms: [{
        type: 'sort',
        target: 'y',
        order: 'descending'
    }]
    };
    var layout3 = {
    title : {text: '<b>Trip Count per Hour of the Day</b>'},
    xaxis : {
        title : {text : 'Hour of the Day'},
        tickvals : uniqueHours,
        ticktext : amPM
    },
    yaxis : { title : {text: 'Number of Trips'} }
    };
    var data3 = [trace3];
    Plotly.newPlot('bar_hour', data3, layout3);

    // ==================================
    // ==================================
    // --- POPULAR STATIONS: ---
    // ==================================
    // MOST COMMON START STATIONS (TRACE 4)
    var startStations = data.map(x => x['Start Station']);

    // var uniqueStart = [...new Set(startStations)];
    var startCounts = {};
    for (var i = 0; i < startStations.length; i++) {
    startCounts[startStations[i]] = 1 + (startCounts[startStations[i]] || 0);
    };
    // console.log(startCounts)
    var topStartStations = Object.keys(startCounts).map(function(key) {
    return [key, startCounts[key]];
        });
    
    topStartStations.sort(function(first, second) {
    return second[1] - first[1];
    });
    var top10Start = topStartStations.slice(0,10);

    var top10StartNames = [];
    var top10StartCounts = [];
    for (var i=0; i<top10Start.length; i++) {
    top10StartNames.push(top10Start[i][0]);
    top10StartCounts.push(top10Start[i][1]);
    };
    var trace4 = {
    x : top10StartNames,
    y : top10StartCounts,
    text : top10StartCounts.map(x => 'Trip Count : ' + x),
    type : 'bar',
    transforms: [{
        type: 'sort',
        target: 'y',
        order: 'descending'
    }]
    };
    var layout4 = {
    title : {text: '<b>Top 10 Start Stations</b>'},
    xaxis : {
        title : {text : 'Start Station'},
        tickfont : { size : 8},
        tickangle: 30,
        // tickvals : uniqueHours,
        // ticktext : amPM
    },
    yaxis : { title : {text: 'Number of Trips'} }
    };
    var data4 = [trace4];
    Plotly.newPlot('bar_startStation', data4, layout4);
    // console.log(top10StartNames)
    // console.log(top10StartCounts)
    
    // ==================================
    // MOST COMMON END STATIONS (TRACE 5)
    var endStations = data.map(x => x['End Station']);

    // var uniqueStart = [...new Set(startStations)];
    var endCounts = {};
    for (var i = 0; i < endStations.length; i++) {
    endCounts[endStations[i]] = 1 + (endCounts[endStations[i]] || 0);
    };
    // console.log(startCounts)
    var topEndStations = Object.keys(endCounts).map(function(key) {
    return [key, endCounts[key]];
        });
    
    topEndStations.sort(function(first, second) {
    return second[1] - first[1];
    });
    var top10End = topEndStations.slice(0,10);

    var top10EndNames = [];
    var top10EndCounts = [];
    for (var i=0; i<top10End.length; i++) {
    top10EndNames.push(top10End[i][0]);
    top10EndCounts.push(top10End[i][1]);
    };
    var trace5 = {
    x : top10EndNames,
    y : top10EndCounts,
    text : top10EndCounts.map(x => 'Trip Count : ' + x),
    type : 'bar',
    transforms: [{
        type: 'sort',
        target: 'y',
        order: 'descending'
    }]
    };
    var layout5 = {
    title : {text: '<b>Top 10 End Stations</b>'},
    xaxis : {
        title : {text : 'End Station'},
        tickfont : { size : 8},
        tickangle: 30,
        // tickvals : uniqueHours,
        // ticktext : amPM
    },
    yaxis : { title : {text: 'Number of Trips'} }
    };
    var data5 = [trace5];
    Plotly.newPlot('bar_endStation', data5, layout5);

    // ==================================
    // MOST COMMON START & END STATIONS (TRACE 6)
    var startEnd = [];
    for (var i=0; i<startStations.length; i++) {
    startEnd.push([startStations[i],endStations[i]])
    };
    // console.log(startEnd)
    var startEndCounts = {};
    for (var i = 0; i < startEnd.length; i++) {
    startEndCounts[startEnd[i]] = 1 + (startEndCounts[startEnd[i]] || 0);
    };
    // console.log(startEndCounts)
    var topStartEndStations = Object.keys(startEndCounts).map(function(key) {
    return [key, startEndCounts[key]];
        });
    
    topStartEndStations.sort(function(first, second) {
    return second[1] - first[1];
    });
    var top10StartEnd = topStartEndStations.slice(0,10);

    var top10StartEndNames = [];
    var top10StartEndCounts = [];
    for (var i=0; i<top10StartEnd.length; i++) {
    top10StartEndNames.push(top10StartEnd[i][0]);
    top10StartEndCounts.push(top10StartEnd[i][1]);
    };
    // console.log(top10StartEndNames)
    // console.log(top10StartEndCounts)

    // xAxisLabels = [];
    // top10StartEndNames.forEach((d) => {
    //   var splitted = d.split(',')
    //   var splitStr = splitted[0]+'\n'+splitted[1]
    //   xAxisLabels.push(splitStr)
    // });
    var xAxisLabels = [];
    top10StartEndNames.forEach((d) => {
    var splitted = d.split(',')
    xAxisLabels.push(splitted[0]+',')
    xAxisLabels.push(splitted[1])
    });
    var trace6 = {
    x : top10StartEndNames,
    y : top10StartEndCounts,
    text : top10StartEndCounts.map(x => 'Trip Count : ' + x),
    hovertemplate: "%{text}<br>Station : %{x}",
    type : 'bar',
    transforms: [{
        type: 'sort',
        target: 'y',
        order: 'descending'
    }]
    };
    var layout6 = {
    title : {text: '<b>Top 10 Start-End Stations</b>'},
    xaxis : {
        title : {text : 'Start and End Station'},
        showticklabels:false
    },
    yaxis : { title : {text: 'Number of Trips'} }
    }
    var data6 = [trace6];
    Plotly.newPlot('bar_startEndStation', data6, layout6);

    // ===========================
    // TRIP DURATION
    var tripTotal = +(d3.select('#tripSum').text().slice(17,35).trim())
    var tripAverage = +(d3.select('#tripSum').text().slice(101,160).trim())


    // ==================================
    // USER TYPES:
    var subs = +(d3.select('#userTypes').text().slice(14,25).trim())
//   var custs = +(d3.select('#userTypes').text().slice(55,).trim())
    var custsIDX = d3.select('#userTypes').text().search('Customers')
    var custs = +(d3.select('#userTypes').text().slice(custsIDX+12,).trim())
    d3.select('#userTypes').text().slice(36+12,)
    var userTypes = ['Subscriber','Customer']
    var userCounts = [subs, custs]
    var traceUser = {
    x : userTypes,
    y : userCounts,
    // text : month_counts,
    text : userCounts.map(x => 'User Count : ' + x),
    type : 'bar',
    transforms: [{
        type: 'sort',
        target: 'y',
        order: 'descending'
    }]
    };
    var layoutUser = {
    title : {text: '<b>User Counts</b>'},
    xaxis : { title : {text: 'User Type'} },
    yaxis : { title : {text: 'Number of Users'} }
    };
    var dataUser = [traceUser];
    Plotly.newPlot('bar_userTypes', dataUser, layoutUser);

    // ==================================
    // ONLY FOR CHICAGO AND NYC:
    if (city === 'chicago' || city === 'new york city') {
        // GENDERS:
        var male = +(d3.select('#genders').text().slice(7,20).trim())

        var femaleIDX = d3.select('#genders').text().search('Female')
        var female = +(d3.select('#genders').text().slice(femaleIDX+9,).trim())
        var genderTypes = ['Male','Female']
        var genderCounts = [male,female]
        console.log(genderCounts)

        var traceGender = {
            x : genderTypes,
            y : genderCounts,
            // text : month_counts,
            text : genderCounts.map(x => 'Gender Count : ' + x),
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layoutGender = {
            title : {text: '<b>Gender Counts</b>'},
            xaxis : { title : {text: 'Gender'} },
            yaxis : { title : {text: 'Number of Users'} }
            };
        var dataGender = [traceGender];
        Plotly.newPlot('bar_gender', dataGender, layoutGender);

        //==========================
        // COMMON BIRTH YEARS
        var birthYears = data.map(x => x['Birth Year']);

        // var uniqueStart = [...new Set(startStations)];
        var birthCounts = {};
        for (var i = 0; i < birthYears.length; i++) {
            birthCounts[birthYears[i]] = 1 + (birthCounts[birthYears[i]] || 0);
        };
        // console.log(startCounts)
        var topBirthYears = Object.keys(birthCounts).map(function(key) {
            return [key, birthCounts[key]];
            });
        
        topBirthYears.sort(function(first, second) {
            return second[1] - first[1];
            });
        var top10Birth = topBirthYears.slice(0,10);

        var top10BirthNames = [];
        var top10BirthCounts = [];
        for (var i=0; i<top10Start.length; i++) {
            top10BirthNames.push(top10Birth[i][0]);
            top10BirthCounts.push(top10Birth[i][1]);
        };

        var traceG = {
            x : top10BirthNames,
            y : top10BirthCounts,
            text : top10BirthCounts.map(x => 'User Count : ' + x),
            type : 'bar',
            transforms: [{
                type: 'sort',
                target: 'y',
                order: 'descending'
            }]
        };
        var layoutG = {
            title : {text: '<b>Top 10 Birth Years</b>'},
            xaxis : {title : {text : 'Birth Year'} },
            yaxis : { title : {text: 'Number of Users'} }
            };
        var dataG = [traceG];
        Plotly.newPlot('bar_birth', dataG, layoutG);
    }; //Ends if city=chicago or nyc
    

}); //Ends d3.csv()