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
        MEDIAN_ANNUAL_INCOME = 575 * 52;
        suburbs = null;
        info = L.control();
        info.onAdd = function(map) {
            _$rapyd$_unbindAll(this, true);
            this._div = L.DomUtil.create("div", "info");
            this.update();
            return this._div;
        };
        info.update = function(props) {
            _$rapyd$_unbindAll(this, true);
            var message, message, message;
            if (props) {
                message = "<h4>" + props.name + "</h4>Some stats such as suburb area and population";
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
            for (i = 0; i < len(LABELS); i++) {
                div.innerHTML += '<i style="background:' + getColor(BINS[i]) + '"></i> ' + LABELS[i] + "<br>";
            }
            return div;
        };
        legend.addTo(map);
        function getColor(x) {
            _$rapyd$_unbindAll(this, true);
            var i, grade;
            var _$rapyd$_Iter5 = enumerate(BINS);
            for (var _$rapyd$_Index5 = 0; _$rapyd$_Index5 < _$rapyd$_Iter5.length; _$rapyd$_Index5++) {
                _$rapyd$_Unpack = _$rapyd$_Iter5[_$rapyd$_Index5];
                i = _$rapyd$_Unpack[0];
                grade = _$rapyd$_Unpack[1];
                if (x <= grade) {
                    return COLORS[i];
                }
            }
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
        function style(feature) {
            _$rapyd$_unbindAll(this, true);
            var grossAnnualIncome, propertyType, numBedrooms, weeklyRent, f, c;
            grossAnnualIncome = int_to_dollar_str($("#income").val(), inverse = true);
            propertyType = $("#propertyType").val();
            numBedrooms = $("#numBedrooms").val();
            weeklyRent = feature.properties[propertyType][numBedrooms];
            console.log("grossAnnualIncome=", grossAnnualIncome);
            console.log("propertyType, numBedrooms, weeklyRent=", propertyType, numBedrooms, weeklyRent);
            f = 52 * weeklyRent / grossAnnualIncome;
            c = getColor(f);
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
            info.update(layer.feature.properties);
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
            el = $("<label>&larr; NZ median annual income (" + int_to_dollar_str(MEDIAN_ANNUAL_INCOME) + ")</label>").css("bottom", MEDIAN_ANNUAL_INCOME / range * 100 + "%");
            $("#slider-vertical").append(el);
        });
        $(function() {
            _$rapyd$_unbindAll(this, true);
            $("#propertyType").selectable({
                "selected": function(event, ui) {
                    _$rapyd$_unbindAll(this, true);
                    $("#propertyType").val(ui.selected.id);
                    suburbs.setStyle(style);
                }
            });
        });
        item = $("#propertyType li:eq(1)");
        item.addClass("ui-selected");
        $("#propertyType").val(item[0].id);
        $(function() {
            _$rapyd$_unbindAll(this, true);
            $("#numBedrooms").selectable({
                "selected": function(event, ui) {
                    _$rapyd$_unbindAll(this, true);
                    $("#numBedrooms").val(ui.selected.id);
                    suburbs.setStyle(style);
                }
            });
        });
        item = $("#numBedrooms li:eq(1)");
        item.addClass("ui-selected");
        $("#numBedrooms").val(item[0].id);
    }

    makeMap();
})();