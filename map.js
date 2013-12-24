(function(){
    function _$rapyd$_bind(fn, thisArg) {
        if (fn.orig) fn = fn.orig;
        var ret = function() {
            return fn.apply(thisArg, arguments);
        }
        ret.orig = fn;
        return ret;
    }
    function _$rapyd$_unbindAll(thisArg, rebind) {
        for (var p in thisArg) {
            if (thisArg[p] && thisArg[p].orig) {
                if (rebind) thisArg[p] = _$rapyd$_bind(thisArg[p], thisArg);
                else thisArg[p] = thisArg[p].orig;
            }
        }
    }
    function reversed(arr) {
        var tmp = [];
        for (var i = arr.length - 1; i >= 0; i--) {
            tmp.push(arr[i]);
        }
        return tmp;
    }
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
    function enumerate(item) {
        var arr = [];
        for (var i = 0; i < item.length; i++) {
            arr[arr.length] = [i, item[i]];
        }
        return arr;
    }
    _$rapyd$_unbindAll(this, true);
    var JSON, str;
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

    function ValueError(message){
        var self = this;
        _$rapyd$_unbindAll(this, true);
        self.name = "ValueError";
        self.message = message;
    };
    ValueError.prototype = new Error();
    ValueError.prototype.constructor = ValueError;
    _$rapyd$_unbindAll(ValueError.prototype);

    String.prototype.find = Array.prototype.indexOf;

    String.prototype.strip = String.prototype.trim;

    String.prototype.lstrip = String.prototype.trimLeft;

    String.prototype.rstrip = String.prototype.trimRight;

    String.prototype.join = function(iterable) {
        _$rapyd$_unbindAll(this, true);
        return iterable.join(this);
    };

    String.prototype.zfill = function(size) {
        _$rapyd$_unbindAll(this, true);
        var s, s;
        s = this;
        while (s.length < size) {
            s = "0" + s;
        }
        return s;
    };

    function list(iterable) {
        if (typeof iterable === "undefined") iterable = [];
        _$rapyd$_unbindAll(this, true);
        var result, i;
        result = [];
        var _$rapyd$_Iter0 = iterable;
        for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
            i = _$rapyd$_Iter0[_$rapyd$_Index0];
            result.append(i);
        }
        return result;
    }

    Array.prototype.append = Array.prototype.push;

    Array.prototype.find = Array.prototype.indexOf;

    Array.prototype.index = function(index) {
        _$rapyd$_unbindAll(this, true);
        var val;
        val = this.find(index);
        if (val == -1) {
            throw new ValueError(str(index) + " is not in list");
        }
        return val;
    };

    Array.prototype.insert = function(index, item) {
        _$rapyd$_unbindAll(this, true);
        this.splice(index, 0, item);
    };

    Array.prototype.pop = function(index) {
        if (typeof index === "undefined") index = this.length - 1;
        _$rapyd$_unbindAll(this, true);
        return this.splice(index, 1)[0];
    };

    Array.prototype.extend = function(array2) {
        _$rapyd$_unbindAll(this, true);
        this.push.apply(this, array2);
    };

    Array.prototype.remove = function(item) {
        _$rapyd$_unbindAll(this, true);
        var index;
        index = this.find(item);
        this.splice(index, 1);
    };

    Array.prototype.copy = function() {
        _$rapyd$_unbindAll(this, true);
        return this.slice(0);
    };

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
        _$rapyd$_unbindAll(this, true);
        return arr.map(oper);
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
        _$rapyd$_unbindAll(this, true);
        return arr.filter(oper);
    }

    function dict(iterable) {
        _$rapyd$_unbindAll(this, true);
        var result, key;
        result = {};
        var _$rapyd$_Iter1 = iterable;
        for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
            key = _$rapyd$_Iter1[_$rapyd$_Index1];
            result[key] = iterable[key];
        }
        return result;
    }

    if (typeof Object.getOwnPropertyNames !== "function") {
        dict.keys = function(hash) {
            _$rapyd$_unbindAll(this, true);
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
            _$rapyd$_unbindAll(this, true);
            return Object.getOwnPropertyNames(hash);
        };
    }

    dict.values = function(hash) {
        _$rapyd$_unbindAll(this, true);
        var vals, key;
        vals = [];
        var _$rapyd$_Iter2 = dict.keys(hash);
        for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
            key = _$rapyd$_Iter2[_$rapyd$_Index2];
            vals.append(hash[key]);
        }
        return vals;
    };

    dict.items = function(hash) {
        _$rapyd$_unbindAll(this, true);
        var items, key;
        items = [];
        var _$rapyd$_Iter3 = dict.keys(hash);
        for (var _$rapyd$_Index3 = 0; _$rapyd$_Index3 < _$rapyd$_Iter3.length; _$rapyd$_Index3++) {
            key = _$rapyd$_Iter3[_$rapyd$_Index3];
            items.append([key, hash[key]]);
        }
        return items;
    };

    dict.copy = dict;

    dict.clear = function(hash) {
        _$rapyd$_unbindAll(this, true);
        var key;
        var _$rapyd$_Iter4 = dict.keys(hash);
        for (var _$rapyd$_Index4 = 0; _$rapyd$_Index4 < _$rapyd$_Iter4.length; _$rapyd$_Index4++) {
            key = _$rapyd$_Iter4[_$rapyd$_Index4];
            delete hash[key];
        }
    };

    function makeMap() {
        _$rapyd$_unbindAll(this, true);
        var map, tilesURL, BINS, LABELS, COLORS, MEDIAN_ANNUAL_INCOME, suburbs, info, legend, item, item;
        map = L.map("map").setView([ -36.84041, 174.73986 ], 12);
        tilesURL = "http://{s}.tiles.mapbox.com/v3/github.map-xgq2svrz/{z}/{x}/{y}.png";
        L.tileLayer(tilesURL).addTo(map);
        map.attributionControl.setPrefix("");
        BINS = [ 0, .25, .5, .75, 1e10 ];
        LABELS = [ "No data", "0&ndash;25% (affordable)", "26&ndash;50%", "51&ndash;75%", "76%+" ];
        COLORS = reversed([ "#d7191c", "#fdae61", "#abdda4", "#2b83ba", "gray" ]);
        MEDIAN_ANNUAL_INCOME = 882 * 52;
        suburbs = null;
        info = L.control();
        info.onAdd = function(map) {
            _$rapyd$_unbindAll(this, true);
            this._div = L.DomUtil.create("div", "info");
            this.update();
            return this._div;
        };
        info.update = function(feature) {
            if (typeof feature === "undefined") feature = null;
            _$rapyd$_unbindAll(this, true);
            var message, message, message;
            if (feature) {
                message = "<h4>" + feature.properties.name + "</h4>" + "Weekly rent per bedroom: " + getWeeklyRent(feature, string = true) + "<br>" + "Fraction of annual income: " + getRentFraction(feature, string = true) + "<br>";
            } else {
                message = "<h4>Suburb Info</h4>Hover over a suburb";
            }
            message += "<br>";
            this._div.innerHTML = message;
        };
        info.addTo(map);
        legend = L.control({
            position: "bottomright"
        });
        legend.onAdd = function(map) {
            _$rapyd$_unbindAll(this, true);
            var div, i;
            div = L.DomUtil.create("div", "info legend");
            var _$rapyd$_Iter5 = reversed(range(len(LABELS)));
            for (var _$rapyd$_Index5 = 0; _$rapyd$_Index5 < _$rapyd$_Iter5.length; _$rapyd$_Index5++) {
                i = _$rapyd$_Iter5[_$rapyd$_Index5];
                div.innerHTML += '<i style="background:' + getColor(BINS[i]) + '"></i> ' + LABELS[i] + "<br>";
            }
            return div;
        };
        legend.addTo(map);
        function getGrossAnnualIncome(string) {
            if (typeof string === "undefined") string = false;
            _$rapyd$_unbindAll(this, true);
            var result, result;
            result = $("#income").val();
            if (!string) {
                result = int_to_dollar_str(result, inverse = true);
            }
            return result;
        }
        function getWeeklyRent(feature, string) {
            if (typeof string === "undefined") string = false;
            _$rapyd$_unbindAll(this, true);
            var propertyType, numBedrooms, result, result, result, result;
            propertyType = $("#property-type").val();
            numBedrooms = $("#num-bedrooms").val();
            result = feature.properties[propertyType][numBedrooms];
            if (result >= 0) {
                if (string) {
                    result = int_to_dollar_str(result);
                }
            } else {
                console.log("string=", string);
                if (string) {
                    result = "No data";
                } else {
                    result = -1;
                }
            }
            return result;
        }
        function getRentFraction(feature, string, ndigits) {
            if (typeof string === "undefined") string = false;
            if (typeof ndigits === "undefined") ndigits = 2;
            _$rapyd$_unbindAll(this, true);
            var result, result, result, result;
            result = 52 * getWeeklyRent(feature) / getGrossAnnualIncome();
            if (result >= 0) {
                if (string) {
                    result = parseInt(result * 100) + "%";
                } else {
                    result = parseFloat(result.toFixed(ndigits));
                }
            } else {
                if (string) {
                    result = "No data";
                }
            }
            return result;
        }
        function int_to_dollar_str(x, inverse) {
            if (typeof inverse === "undefined") inverse = false;
            _$rapyd$_unbindAll(this, true);
            if (!inverse) {
                return "$" + x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            } else {
                return parseInt(x.replace("$", "").replace(",", ""));
            }
        }
        function getColor(x) {
            _$rapyd$_unbindAll(this, true);
            var i, grade;
            var _$rapyd$_Iter6 = enumerate(BINS);
            for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
                _$rapyd$_Unpack = _$rapyd$_Iter6[_$rapyd$_Index6];
                i = _$rapyd$_Unpack[0];
                grade = _$rapyd$_Unpack[1];
                if (x <= grade) {
                    return COLORS[i];
                }
            }
        }
        function style(feature) {
            _$rapyd$_unbindAll(this, true);
            var c;
            c = getColor(getRentFraction(feature));
            return {
                "fillColor": c,
                "fillOpacity": .7,
                "color": c,
                "weight": 1,
                "opacity": .7
            };
        }
        function highlightFeature(e) {
            _$rapyd$_unbindAll(this, true);
            var layer;
            layer = e.target;
            layer.setStyle({
                "weight": 5,
                "color": "#666",
                "dashArray": "",
                "fillOpacity": .7
            });
            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }
            info.update(layer.feature);
        }
        function resetHighlight(e) {
            _$rapyd$_unbindAll(this, true);
            var layer;
            layer = e.target;
            suburbs.resetStyle(layer);
            info.update();
        }
        function zoomToFeature(e) {
            _$rapyd$_unbindAll(this, true);
            map.fitBounds(e.target.getBounds());
        }
        function onEachFeature(feature, layer) {
            _$rapyd$_unbindAll(this, true);
            layer.on({
                "mouseover": highlightFeature,
                "mouseout": resetHighlight,
                "click": zoomToFeature
            });
        }
        $.getJSON("test.geojson", function(collection) {
            _$rapyd$_unbindAll(this, true);
            suburbs = L.geoJson(collection, {
                style: style,
                onEachFeature: onEachFeature
            }).addTo(map);
        });
        $(function() {
            _$rapyd$_unbindAll(this, true);
            var sv, min, range, el;
            $("#slider-vertical").slider({
                "orientation": "vertical",
                "range": "min",
                "min": 100,
                "max": 1e5,
                "value": MEDIAN_ANNUAL_INCOME,
                "step": 100,
                "slide": function(event, ui) {
                    _$rapyd$_unbindAll(this, true);
                    $("#income").val(int_to_dollar_str(ui.value));
                    suburbs.setStyle(style);
                }
            });
            sv = $("#slider-vertical");
            $("#income").val(int_to_dollar_str(sv.slider("value")));
            min = sv.slider("option", "min");
            range = sv.slider("option", "max") - min;
            el = $('<label><span id="arrow">&larr;</span>' + "Median annual income<br>of employed Aucklanders<br>(" + int_to_dollar_str(MEDIAN_ANNUAL_INCOME) + ")</label>").css("bottom", MEDIAN_ANNUAL_INCOME / range * 100 + "%");
            $("#slider-vertical").append(el);
        });
        $(function() {
            _$rapyd$_unbindAll(this, true);
            $("#property-type").selectable({
                "selected": function(event, ui) {
                    _$rapyd$_unbindAll(this, true);
                    $("#property-type").val(ui.selected.id);
                    suburbs.setStyle(style);
                }
            });
        });
        item = $("#property-type li:eq(1)");
        item.addClass("ui-selected");
        $("#property-type").val(item[0].id);
        $(function() {
            _$rapyd$_unbindAll(this, true);
            $("#num-bedrooms").selectable({
                "selected": function(event, ui) {
                    _$rapyd$_unbindAll(this, true);
                    $("#num-bedrooms").val(ui.selected.id);
                    suburbs.setStyle(style);
                }
            });
        });
        item = $("#num-bedrooms li:eq(1)");
        item.addClass("ui-selected");
        $("#num-bedrooms").val(item[0].id);
    }

    makeMap();
})();