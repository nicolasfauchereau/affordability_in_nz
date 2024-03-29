(function(){
    function range(start, stop, step) {
        if (arguments.length <= 1) {
            stop = start || 0;
            start = 0;
        }
        step = arguments[2] || 1;
        var length = Math.max (Math.ceil ((stop - start) / step) , 0);
        var idx = 0;
        var range = new Array(length);
        while (idx < length) {
            range[idx++] = start;
            start += step;
        }
        return range;
    }
    function len(obj) {
        if (obj instanceof Array || typeof obj === "string") return obj.length;
        else {
            var count = 0;
            for (var i in obj) {
                if (obj.hasOwnProperty(i)) count++;
            }
            return count;
        }
    }
    function _$rapyd$_in(val, arr) {
        if (arr instanceof Array || typeof arr === "string") return arr.indexOf(val) != -1;
        else {
            for (i in arr) {
                if (arr.hasOwnProperty(i) && i === val) return true;
            }
            return false;
        }
    }
    function dir(item) {
        var arr = [];
        for (var i in item) {
            arr.push(i);
        }
        return arr;
    }
    function _$rapyd$_extends(child, parent) {
        child.prototype = new parent;
        child.prototype.constructor = child;
    }
    function reversed(arr) {
        var tmp = [];
        for (var i = arr.length - 1; i >= 0; i--) {
            tmp.push(arr[i]);
        }
        return tmp;
    }
    function enumerate(item) {
        var arr = [];
        for (var i = 0; i < item.length; i++) {
            arr[arr.length] = [i, item[i]];
        }
        return arr;
    }
    var JSON, str, data, lon, lat, maxBounds, _$rapyd$_Unpack, markerLatLon0, markerLatLon1, medianAnnualIncome, zoom, rentByNbedroomsByAu, M, MIndexByAu, aus, spinner;
            JSON = JSON || {};
    if (!JSON.stringify) {
        
    JSON.stringify = function(obj) {
        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string")
                obj = '"' + obj + '"';
            if (t == "function")
                return; // return undefined
            else
                return String(obj);
        } else {
            // recurse array or object
            var n, v, json = []
            var arr = (obj && obj.constructor == Array);
            for (n in obj) {
                v = obj[n];
                t = typeof (v);
                if (t != "function" && t != "undefined") {
                    if (t == "string")
                        v = '"' + v + '"';
                    else if ((t == "object" || t == "function") && v !== null)
                        v = JSON.stringify(v);
                    json.push((arr ? "" : '"' + n + '":') + String(v));
                }
            }
            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    };
    ;
    }
    str = JSON.stringify;
    function kwargs(f) {
        var argNames;
        argNames = f.toString().match(/\(([^\)]+)/)[1];
        argNames = argNames ? argNames.split(",").map(function(s) {
            return s.trim();
        }) : [];
        return function() {
            var args, kw, i;
            args = [].slice.call(arguments);
            if (args.length && args.length < f.length) {
                kw = args.pop();
                if (typeof kw == "object") {
                    for (i = 0; i < len(argNames); i++) {
                        if (_$rapyd$_in(argNames[i], dir(kw))) {
                            args[i] = kw[argNames[i]];
                        }
                    }
                } else {
                    args.push(kw);
                }
            }
            return f.apply(f, args);
        };
    }
    function IndexError(message){
        var self = this;
        if (typeof message === "undefined") message = "list index out of range";
        self.name = "IndexError";
        self.message = message;
    };

    _$rapyd$_extends(IndexError, Error);

    function TypeError(message){
        var self = this;
        self.name = "TypeError";
        self.message = message;
    };

    _$rapyd$_extends(TypeError, Error);

    function ValueError(message){
        var self = this;
        self.name = "ValueError";
        self.message = message;
    };

    _$rapyd$_extends(ValueError, Error);

    function AssertionError(message){
        var self = this;
        if (typeof message === "undefined") message = "";
        self.name = "AssertionError";
        self.message = message;
    };

    _$rapyd$_extends(AssertionError, Error);

    if (!Array.prototype.map) {
        
	Array.prototype.map = function(callback, thisArg) {
		var T, A, k;
		if (this == null) {
			throw new TypeError(" this is null or not defined");
		}
		var O = Object(this);
		var len = O.length >>> 0;
		if ({}.toString.call(callback) != "[object Function]") {
			throw new TypeError(callback + " is not a function");
		}
		if (thisArg) {
			T = thisArg;
		}
		A = new Array(len);
		for (var k = 0; k < len; k++) {
			var kValue, mappedValue;
			if (k in O) {
				kValue = O[k];
				mappedValue = callback.call(T, kValue);
				A[k] = mappedValue;
			}
		}
		return A;
	};
	;
    }
    function map(oper, arr) {
        return list(arr.map(oper));
    }
    if (!Array.prototype.filter) {
        
	Array.prototype.filter = function(filterfun, thisArg) {
		"use strict";
		if (this == null) {
			throw new TypeError(" this is null or not defined");
		}
		var O = Object(this);
		var len = O.length >>> 0;
		if ({}.toString.call(filterfun) != "[object Function]") {
			throw new TypeError(filterfun + " is not a function");
		}
		if (thisArg) {
			T = thisArg;
		}
		var A = [];
		var thisp = arguments[1];
		for (var k = 0; k < len; k++) {
			if (k in O) {
				var val = O[k]; // in case fun mutates this
				if (filterfun.call(T, val))
					A.push(val);
			}
		}
		return A;
	};
	;
    }
    function filter(oper, arr) {
        return list(arr.filter(oper));
    }
    function sum(arr, start) {
        if (typeof start === "undefined") start = 0;
        return arr.reduce(function(prev, cur) {
            return prev + cur;
        }, start);
    }
    function deep_eq(a, b) {
        var i;
        "\n    Equality comparison that works with all data types, returns true if structure and\n    contents of first object equal to those of second object\n\n    Arguments:\n        a: first object\n        b: second object\n    ";
        if (a === b) {
            return true;
        }
        if (a instanceof Array && b instanceof Array || a instanceof Object && b instanceof Object) {
            if (a.constructor !== b.constructor || a.length !== b.length) {
                return false;
            }
            var _$rapyd$_Iter0 = dict.keys(a);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                i = _$rapyd$_Iter0[_$rapyd$_Index0];
                if (b.hasOwnProperty(i)) {
                    if (!deep_eq(a[i], b[i])) {
                        return false;
                    }
                } else {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    String.prototype.find = Array.prototype.indexOf;
    String.prototype.strip = String.prototype.trim;
    String.prototype.lstrip = String.prototype.trimLeft;
    String.prototype.rstrip = String.prototype.trimRight;
    String.prototype.join = function(iterable) {
        return iterable.join(this);
    };
    String.prototype.zfill = function(size) {
        var s;
        s = this;
        while (s.length < size) {
            s = "0" + s;
        }
        return s;
    };
    function list(iterable) {
        if (typeof iterable === "undefined") iterable = [];
        var result, i;
        result = [];
        var _$rapyd$_Iter1 = iterable;
        for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
            i = _$rapyd$_Iter1[_$rapyd$_Index1];
            result.append(i);
        }
        return result;
    }
    Array.prototype.append = Array.prototype.push;
    Array.prototype.find = Array.prototype.indexOf;
    Array.prototype.index = function(index) {
        var val;
        val = this.find(index);
        if (val == -1) {
            throw new ValueError(str(index) + " is not in list");
        }
        return val;
    };
    Array.prototype.insert = function(index, item) {
        this.splice(index, 0, item);
    };
    Array.prototype.pop = function(index) {
        if (typeof index === "undefined") index = this.length - 1;
        return this.splice(index, 1)[0];
    };
    Array.prototype.extend = function(array2) {
        this.push.apply(this, array2);
    };
    Array.prototype.remove = function(item) {
        var index;
        index = this.find(item);
        this.splice(index, 1);
    };
    Array.prototype.copy = function() {
        return this.slice(0);
    };
    function dict(iterable) {
        var result, key;
        result = {};
        var _$rapyd$_Iter2 = iterable;
        for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
            key = _$rapyd$_Iter2[_$rapyd$_Index2];
            result[key] = iterable[key];
        }
        return result;
    }
    if (typeof Object.getOwnPropertyNames !== "function") {
        dict.keys = function(hash) {
            var keys;
            keys = [];
            
        for (var x in hash) {
            if (hash.hasOwnProperty(x)) {
                keys.push(x);
            }
        }
        ;
            return keys;
        };
    } else {
        dict.keys = function(hash) {
            return Object.getOwnPropertyNames(hash);
        };
    }
    dict.values = function(hash) {
        var vals, key;
        vals = [];
        var _$rapyd$_Iter3 = dict.keys(hash);
        for (var _$rapyd$_Index3 = 0; _$rapyd$_Index3 < _$rapyd$_Iter3.length; _$rapyd$_Index3++) {
            key = _$rapyd$_Iter3[_$rapyd$_Index3];
            vals.append(hash[key]);
        }
        return vals;
    };
    dict.items = function(hash) {
        var items, key;
        items = [];
        var _$rapyd$_Iter4 = dict.keys(hash);
        for (var _$rapyd$_Index4 = 0; _$rapyd$_Index4 < _$rapyd$_Iter4.length; _$rapyd$_Index4++) {
            key = _$rapyd$_Iter4[_$rapyd$_Index4];
            items.append([key, hash[key]]);
        }
        return items;
    };
    dict.copy = dict;
    dict.clear = function(hash) {
        var key;
        var _$rapyd$_Iter5 = dict.keys(hash);
        for (var _$rapyd$_Index5 = 0; _$rapyd$_Index5 < _$rapyd$_Iter5.length; _$rapyd$_Index5++) {
            key = _$rapyd$_Iter5[_$rapyd$_Index5];
            delete hash[key];
        }
    };
    data = $.parseJSON($("#data").html());
    lon = data["lon"];
    lat = data["lat"];
    maxBounds = data["maxBounds"];
    _$rapyd$_Unpack = data["markerLatLons"];
    markerLatLon0 = _$rapyd$_Unpack[0];
    markerLatLon1 = _$rapyd$_Unpack[1];
    medianAnnualIncome = data["medianAnnualIncome"];
    zoom = data["zoom"];
    rentByNbedroomsByAu = null;
    M = null;
    MIndexByAu = null;
    aus = null;
    spinner = new Spinner().spin($("#map").get(0));
    $.when($.getJSON(data["shapesFile"]), $.getJSON(data["rentsFile"]), $.getJSON(data["commuteCostsFile"])).done(function(a, b, c) {
        aus = a[0];
        rentByNbedroomsByAu = b[0];
        MIndexByAu = c[0]["index_by_name"];
        M = c[0]["matrix"];
        spinner.stop();
        makeUI();
    });
    function sum(a, b) {
        var result;
        if (a !== null && b !== null) {
            result = a + b;
        } else if (a !== null) {
            result = a;
        } else if (b !== null) {
            result = b;
        } else {
            result = null;
        }
        return result;
    }
    function numToDollarStr(x, inverse) {
        if (typeof inverse === "undefined") inverse = false;
        var dollars;
        if (!inverse) {
            if (x === null) {
                return "n/a";
            }
            dollars = x.toFixed(0);
            dollars = dollars.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            return "$" + dollars;
        } else {
            if (x == "n/a") {
                return null;
            }
            return parseInt(x.replace("$", "").replace(",", ""));
        }
    }
    function makeUI() {
        var WEEKLY_CAR_OWN_COST, item, map, BINS, LABELS, OPACITY, COLORS_RGB, COLORS, hex, c, legend, info, workMarker0, workMarker1, workMarkers, marker;
        WEEKLY_CAR_OWN_COST = 2228 / 52;
        $(function() {
            var sv, min, range, el;
            $("#income-slider").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 100,
                "max": 2e5,
                "value": medianAnnualIncome,
                "step": 100,
                "slide": function(event, ui) {
                    $("#income").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    aus.setStyle(auStyle);
                }
            });
            sv = $("#income-slider");
            $("#income").val(numToDollarStr(sv.slider("value")));
            min = sv.slider("option", "min");
            range = sv.slider("option", "max") - min;
            el = $("<label>&#9650;</label><br>").css("left", medianAnnualIncome / range * 100 + "%");
            $("#income-slider").append(el);
        });
        function adjustNumBedroomsRent() {
            var nb, group, nbr, item, x;
            nb = $("#num-bedrooms").val();
            group = $("#num-bedrooms-rent");
            nbr = group.val();
            if (nbr > nb) {
                nbr = nb;
                group.val(nb);
            }
            for (x = 1; x < 6; x++) {
                item = $("#num-bedrooms-rent li[value=" + x + "]");
                if (x == nbr) {
                    item.addClass("ui-selected");
                }
                if (x <= nb) {
                    item.removeClass("blocked");
                } else {
                    item.removeClass("ui-selected");
                    item.addClass("blocked");
                }
                group.selectable({
                    cancel: ".blocked"
                });
            }
        }
        $(function() {
            $("#num-bedrooms").selectable({
                "selected": function(event, ui) {
                    $("#num-bedrooms").val(ui.selected.value);
                    adjustNumBedroomsRent();
                    aus.setStyle(auStyle);
                }
            });
        });
        item = $("#num-bedrooms li:eq(1)");
        item.addClass("ui-selected");
        $("#num-bedrooms").val(item[0].value);
        adjustNumBedroomsRent();
        $(function() {
            $("#num-bedrooms-rent").selectable({
                "selected": function(event, ui) {
                    $("#num-bedrooms-rent").val(ui.selected.value);
                    aus.setStyle(auStyle);
                }
            });
        });
        item = $("#num-bedrooms-rent li:eq(0)");
        item.addClass("ui-selected");
        $("#num-bedrooms-rent").val(item[0].value);
        $(function() {
            $("#mode0").selectable({
                "selected": function(event, ui) {
                    var mode, item, numWorkdays;
                    $("#mode0").val(ui.selected.id);
                    mode = $("#mode0").val();
                    if (mode != "car") {
                        $("#parking0").val("$0");
                        $("#parking-slider0").slider("value", 0);
                    } else {
                        item = $("#num-cars li.ui-selected");
                        if (item.val() == 0) {
                            item.removeClass("ui-selected");
                            $("#num-cars li:eq(1)").addClass("ui-selected");
                            $("#num-cars").val(1);
                        }
                    }
                    numWorkdays = parseInt($("#num-workdays0").val());
                    if (numWorkdays) {
                        aus.setStyle(auStyle);
                    }
                }
            });
        });
        item = $("#mode0 li:eq(1)");
        item.addClass("ui-selected");
        $("#mode0").val(item[0].id);
        $(function() {
            $("#mode1").selectable({
                "selected": function(event, ui) {
                    var mode, item, numWorkdays;
                    $("#mode1").val(ui.selected.id);
                    mode = $("#mode1").val();
                    if (mode != "car") {
                        $("#parking1").val("$0");
                        $("#parking-slider1").slider("value", 0);
                    } else {
                        item = $("#num-cars li.ui-selected");
                        if (item.val() == 0) {
                            item.removeClass("ui-selected");
                            $("#num-cars li:eq(1)").addClass("ui-selected");
                            $("#num-cars").val(1);
                        }
                    }
                    numWorkdays = parseInt($("#num-workdays1").val());
                    if (numWorkdays) {
                        aus.setStyle(auStyle);
                    }
                }
            });
        });
        item = $("#mode1 li:eq(1)");
        item.addClass("ui-selected");
        $("#mode1").val(item[0].id);
        $(function() {
            var s;
            $("#num-workdays-slider0").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 7,
                "value": 5,
                "step": 1,
                "slide": function(event, ui) {
                    $("#num-workdays0").val(ui.value);
                },
                "stop": function(event, ui) {
                    aus.setStyle(auStyle);
                }
            });
            s = $("#num-workdays-slider0");
            $("#num-workdays0").val(s.slider("value"));
        });
        $(function() {
            var s;
            $("#num-workdays-slider1").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 7,
                "value": 0,
                "step": 1,
                "slide": function(event, ui) {
                    $("#num-workdays1").val(ui.value);
                },
                "stop": function(event, ui) {
                    aus.setStyle(auStyle);
                }
            });
            s = $("#num-workdays-slider1");
            $("#num-workdays1").val(s.slider("value"));
        });
        $(function() {
            var s;
            $("#parking-slider0").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 30,
                "value": 0,
                "step": 1,
                "slide": function(event, ui) {
                    $("#parking0").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays;
                    numWorkdays = parseInt($("#num-workdays0").val());
                    if (numWorkdays) {
                        aus.setStyle(auStyle);
                    }
                }
            });
            s = $("#parking-slider0");
            $("#parking0").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            var s;
            $("#parking-slider1").slider({
                "orientation": "horizontal",
                "range": "min",
                "min": 0,
                "max": 30,
                "value": 0,
                "step": 1,
                "slide": function(event, ui) {
                    $("#parking1").val(numToDollarStr(ui.value));
                },
                "stop": function(event, ui) {
                    var numWorkdays;
                    numWorkdays = parseInt($("#num-workdays1").val());
                    if (numWorkdays) {
                        aus.setStyle(auStyle);
                    }
                }
            });
            s = $("#parking-slider1");
            $("#parking1").val(numToDollarStr(s.slider("value")));
        });
        $(function() {
            $("#num-cars").selectable({
                "selected": function(event, ui) {
                    $("#num-cars").val(ui.selected.value);
                    aus.setStyle(auStyle);
                }
            });
        });
        item = $("#num-cars li:eq(0)");
        item.addClass("ui-selected");
        $("#num-cars").val(item[0].value);
        map = L.map("map", {
            "center": [ lat, lon ],
            "zoom": zoom,
            "minZoom": 8,
            "maxZoom": 13,
            "maxBounds": maxBounds
        });
        map.scrollWheelZoom.disable();
        map.attributionControl.setPrefix("");
        BINS = [ 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1e10 ];
        LABELS = [ "n/a", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%+" ];
        OPACITY = 1;
        COLORS_RGB = reversed([ [ 158, 1, 66 ], [ 213, 62, 79 ], [ 244, 109, 67 ], [ 253, 174, 97 ], [ 254, 224, 139 ], [ 230, 245, 152 ], [ 171, 221, 164 ], [ 102, 194, 165 ], [ 50, 136, 189 ], [ 94, 79, 162 ], [ 200, 200, 200 ] ]);
        COLORS = [];
        var _$rapyd$_Iter6 = COLORS_RGB;
        for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
            c = _$rapyd$_Iter6[_$rapyd$_Index6];
            c.append(OPACITY);
            hex = rgbaToHex(c);
            COLORS.append(hex);
        }
        function rgbaToHex(s) {
            var _$rapyd$_Unpack, a, h, result, x;
            _$rapyd$_Unpack = [s.slice(0, -1), s[s.length-1]];
            s = _$rapyd$_Unpack[0];
            a = _$rapyd$_Unpack[1];
            result = "#";
            var _$rapyd$_Iter7 = s;
            for (var _$rapyd$_Index7 = 0; _$rapyd$_Index7 < _$rapyd$_Iter7.length; _$rapyd$_Index7++) {
                x = _$rapyd$_Iter7[_$rapyd$_Index7];
                h = Math.round(a * x + 255 * (1 - a)).toString(16);
                if (len(h) < 2) {
                    h = "0" + h;
                }
                result += h;
            }
            return result;
        }
        legend = L.control({
            "position": "bottomleft"
        });
        legend.onAdd = function(map) {
            var div, n, i;
            div = L.DomUtil.create("div", "legend");
            div.innerHTML = "<h4>Cost as % of income</h4>";
            n = len(BINS);
            for (i = 0; i < n; i++) {
                div.innerHTML += "<span class=\"color\" style=\"background:" + getColor(BINS[n - i - 1]) + "\"></span><span>" + LABELS[n - i - 1] + "</span><br/>";
            }
            return div;
        };
        legend.addTo(map);
        L.control.scale({
            "imperial": false,
            "position": "topleft"
        }).addTo(map);
        info = L.control({
            position: "bottomright"
        });
        info.onAdd = function(map) {
            this._div = L.DomUtil.create("div", "info");
            this.update();
            return this._div;
        };
        info.update = function(feature) {
            if (typeof feature === "undefined") feature = null;
            var income, numBedrooms, numBedroomsRent, rent, _$rapyd$_Unpack, commuteCost, park, car, commuteTime, total, fraction, percent, message;
            if (feature) {
                income = getWeeklyIncome();
                numBedrooms = $("#num-bedrooms").val();
                numBedroomsRent = $("#num-bedrooms-rent").val();
                rent = getWeeklyRent(feature);
                _$rapyd$_Unpack = getWeeklyCommuteCostAndTime(feature);
                commuteCost = _$rapyd$_Unpack[0];
                commuteTime = _$rapyd$_Unpack[1];
                park = getWeeklyParkingCost();
                car = getWeeklyCarOwnCost();
                if (commuteTime !== null) {
                    commuteTime = commuteTime.toFixed(1) + "&nbsp;h";
                } else {
                    commuteTime = "n/a";
                }
                if (rent !== null && commuteCost !== null) {
                    total = rent + commuteCost + park + car;
                    fraction = total / income;
                    percent = (fraction * 100).toFixed(1) + "%";
                } else {
                    total = null;
                    fraction = null;
                    percent = "n/a";
                }
                message = "<h4>" + feature.properties.AU2013_NAM + "</h4>" + "<table>" + "<tr><td>Income per week</td><td>" + numToDollarStr(income, false) + "</td>" + "<tr><td>Rent per week (" + numBedroomsRent + " of " + numBedrooms + " bd)</td><td>" + numToDollarStr(rent, false) + "</td></tr>" + "<tr><td>Commute cost per week</td><td>" + numToDollarStr(commuteCost, false) + "</td></tr>" + "<tr><td>Commute time per week</td><td>" + commuteTime + "</td></tr>" + "<tr><td>Parking cost per week</td><td>" + numToDollarStr(park, false) + "</td></tr>" + "<tr><td>Car cost per week</td><td>" + numToDollarStr(car, false) + "</td></tr>" + "<tr><td>Total cost per week</td><td>" + numToDollarStr(total, false) + "</td></tr>" + "<tr><td>% of weekly income</td><td>" + percent + "</td></tr>" + "</table>";
            } else {
                message = "<h4>Info box</h4>Hover over an area unit";
            }
            this._div.innerHTML = message;
        };
        info.addTo(map);
        workMarker0 = L.marker(markerLatLon0, {
            "draggable": true,
            "title": "Your Work",
            "icon": L.mapbox.marker.icon({
                "marker-color": COLORS[COLORS.length-2],
                "marker-symbol": "y"
            })
        }).addTo(map);
        workMarker1 = L.marker(markerLatLon1, {
            "draggable": true,
            "title": "Partner's Work",
            "icon": L.mapbox.marker.icon({
                "marker-color": COLORS[COLORS.length-2],
                "marker-symbol": "p"
            })
        }).addTo(map);
        workMarkers = [ workMarker0, workMarker1 ];
        var _$rapyd$_Iter8 = workMarkers;
        for (var _$rapyd$_Index8 = 0; _$rapyd$_Index8 < _$rapyd$_Iter8.length; _$rapyd$_Index8++) {
            marker = _$rapyd$_Iter8[_$rapyd$_Index8];
            marker.bindPopup("<h4>" + marker.options.title + "</h4>Undefined");
            marker.on("drag", function(e) {
                setWorkPopup(this);
            });
            marker.on("dragend", function(e) {
                aus.setStyle(auStyle);
            });
        }
        function getWorkAuName(marker) {
            var latLon, layer, auName;
            latLon = marker.getLatLng();
            try {
                layer = leafletPip.pointInLayer(latLon, aus, true)[0];
            } catch (_$rapyd$_Exception) {
                return null;
            }
            if (layer) {
                auName = layer.feature.properties.AU2013_NAM;
            } else {
                auName = null;
            }
            return auName;
        }
        function setWorkPopup(marker) {
            var auName, text;
            auName = getWorkAuName(marker);
            text = "<h4>" + marker.options.title + "</h4>";
            if (auName) {
                text += auName;
            } else {
                text += "Undefined";
            }
            marker.setPopupContent(text);
            marker.openPopup();
        }
        aus = L.geoJson(aus, {
            "style": auStyle,
            "onEachFeature": onEachFeature
        }).addTo(map);
        function getColor(x) {
            var _$rapyd$_Unpack, i, grade;
            var _$rapyd$_Iter9 = enumerate(BINS);
            for (var _$rapyd$_Index9 = 0; _$rapyd$_Index9 < _$rapyd$_Iter9.length; _$rapyd$_Index9++) {
                _$rapyd$_Unpack = _$rapyd$_Iter9[_$rapyd$_Index9];
                i = _$rapyd$_Unpack[0];
                grade = _$rapyd$_Unpack[1];
                if (x <= grade) {
                    return COLORS[i];
                }
            }
            return COLORS[0];
        }
        function auStyle(feature) {
            var c;
            c = getColor(getWeeklyTotalCostFraction(feature));
            return {
                "fillColor": c,
                "fillOpacity": 1,
                "color": "black",
                "weight": .5,
                "opacity": 1
            };
        }
        function highlightFeature(e) {
            var layer;
            layer = e.target;
            layer.setStyle({
                "weight": 2
            });
            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }
            info.update(layer.feature);
        }
        function resetHighlight(e) {
            var layer;
            layer = e.target;
            aus.resetStyle(layer);
            layer._map.closePopup();
            info.update();
        }
        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }
        function onEachFeature(feature, layer) {
            layer.on({
                "mouseover": highlightFeature,
                "mouseout": resetHighlight,
                "click": zoomToFeature
            });
        }
        function getWeeklyIncome() {
            var income;
            income = $("#income").val();
            return numToDollarStr(income, true) / 52;
        }
        function getWeeklyRent(feature) {
            var numBedrooms, numBedroomsRent, auName, rent;
            numBedrooms = $("#num-bedrooms").val();
            numBedroomsRent = $("#num-bedrooms-rent").val();
            auName = feature.properties.AU2013_NAM;
            rent = rentByNbedroomsByAu[auName][numBedrooms];
            if (rent !== null) {
                rent = parseFloat(rent);
                rent *= parseInt(numBedroomsRent) / parseInt(numBedrooms);
            } else {
                rent = null;
            }
            return rent;
        }
        function getWeeklyCommuteCostAndTime(feature) {
            var auName, numWorkdays, mode, workAuName, i, j, _$rapyd$_Unpack, cost, time, totalCost, totalTime, k;
            auName = feature.properties.AU2013_NAM;
            i = MIndexByAu[auName];
            totalCost = 0;
            totalTime = 0;
            for (k = 0; k < 2; k++) {
                numWorkdays = parseInt($("#num-workdays" + str(k)).val());
                if (!numWorkdays) {
                    continue;
                }
                mode = $("#mode" + str(k)).val();
                workAuName = getWorkAuName(workMarkers[k]);
                if (workAuName === null) {
                    continue;
                }
                j = MIndexByAu[workAuName];
                if (j > i) {
                    _$rapyd$_Unpack = [j, i];
                    i = _$rapyd$_Unpack[0];
                    j = _$rapyd$_Unpack[1];
                }
                _$rapyd$_Unpack = M[mode][i][j];
                cost = _$rapyd$_Unpack[0];
                time = _$rapyd$_Unpack[1];
                if (cost === null) {
                    return [null, null];
                }
                totalCost += numWorkdays * cost;
                totalTime += numWorkdays * time;
            }
            return [totalCost, totalTime];
        }
        function getWeeklyCarOwnCost() {
            var numCars;
            numCars = parseInt($("#num-cars").val());
            return numCars * WEEKLY_CAR_OWN_COST;
        }
        function getWeeklyParkingCost() {
            var parking, numWorkdays, totalCost, k;
            totalCost = 0;
            for (k = 0; k < 2; k++) {
                parking = $("#parking" + str(k)).val();
                parking = numToDollarStr(parking, true);
                numWorkdays = parseInt($("#num-workdays" + str(k)).val());
                totalCost += parking * numWorkdays;
            }
            return totalCost;
        }
        function getWeeklyTotalCost(feature) {
            var rent, cc, total;
            rent = getWeeklyRent(feature);
            cc = getWeeklyCommuteCostAndTime(feature)[0];
            if (rent !== null && cc !== null) {
                total = rent + cc + getWeeklyCarOwnCost() + getWeeklyParkingCost();
            } else {
                total = null;
            }
            return total;
        }
        function getWeeklyTotalCostFraction(feature) {
            var total, fraction;
            total = getWeeklyTotalCost(feature);
            if (total !== null) {
                fraction = total / getWeeklyIncome();
            } else {
                fraction = null;
            }
            return fraction;
        }
    }
})();