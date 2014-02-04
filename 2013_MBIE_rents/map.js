(function(){function _$rapyd$_extends(child,parent){child.prototype=new parent;child.prototype.constructor=child}function reversed(arr){var tmp=[];for(var i=arr.length-1;i>=0;i--){tmp.push(arr[i])}return tmp}function range(start,stop,step){if(arguments.length<=1){stop=start||0;start=0}step=arguments[2]||1;var length=Math.max(Math.ceil((stop-start)/step),0);var idx=0;var range=new Array(length);while(idx<length){range[idx++]=start;start+=step}return range}function len(obj){if(obj instanceof Array||typeof obj==="string")return obj.length;else{var count=0;for(var i in obj){if(obj.hasOwnProperty(i))count++}return count}}function enumerate(item){var arr=[];for(var i=0;i<item.length;i++){arr[arr.length]=[i,item[i]]}return arr}var JSON,str,dataFileName;JSON=JSON||{};if(!JSON.stringify){
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
    }str=JSON.stringify;function IndexError(message){var self=this;if(typeof message==="undefined")message="list index out of range";self.name="IndexError";self.message=message};_$rapyd$_extends(IndexError,Error);function TypeError(message){var self=this;self.name="TypeError";self.message=message};_$rapyd$_extends(TypeError,Error);function ValueError(message){var self=this;self.name="ValueError";self.message=message};_$rapyd$_extends(ValueError,Error);function AssertionError(message){var self=this;if(typeof message==="undefined")message="";self.name="AssertionError";self.message=message};_$rapyd$_extends(AssertionError,Error);if(!Array.prototype.map){
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
	}function map(oper,arr){return list(arr.map(oper))}if(!Array.prototype.filter){
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
	}function filter(oper,arr){return list(arr.filter(oper))}function sum(arr,start){if(typeof start==="undefined")start=0;return arr.reduce(function(prev,cur){return prev+cur},start)}function deep_eq(a,b){var i;"\n    Equality comparison that works with all data types, returns true if structure and\n    contents of first object equal to those of second object\n\n    Arguments:\n        a: first object\n        b: second object\n    ";if(a===b){return true}if(a instanceof Array&&b instanceof Array||a instanceof Object&&b instanceof Object){if(a.constructor!==b.constructor||a.length!==b.length){return false}var _$rapyd$_Iter0=dict.keys(a);for(var _$rapyd$_Index0=0;_$rapyd$_Index0<_$rapyd$_Iter0.length;_$rapyd$_Index0++){i=_$rapyd$_Iter0[_$rapyd$_Index0];if(b.hasOwnProperty(i)){if(!deep_eq(a[i],b[i])){return false}}else{return false}}return true}return false}String.prototype.find=Array.prototype.indexOf;String.prototype.strip=String.prototype.trim;String.prototype.lstrip=String.prototype.trimLeft;String.prototype.rstrip=String.prototype.trimRight;String.prototype.join=function(iterable){return iterable.join(this)};String.prototype.zfill=function(size){var s;s=this;while(s.length<size){s="0"+s}return s};function list(iterable){if(typeof iterable==="undefined")iterable=[];var result,i;result=[];var _$rapyd$_Iter1=iterable;for(var _$rapyd$_Index1=0;_$rapyd$_Index1<_$rapyd$_Iter1.length;_$rapyd$_Index1++){i=_$rapyd$_Iter1[_$rapyd$_Index1];result.append(i)}return result}Array.prototype.append=Array.prototype.push;Array.prototype.find=Array.prototype.indexOf;Array.prototype.index=function(index){var val;val=this.find(index);if(val==-1){throw new ValueError(str(index)+" is not in list")}return val};Array.prototype.insert=function(index,item){this.splice(index,0,item)};Array.prototype.pop=function(index){if(typeof index==="undefined")index=this.length-1;return this.splice(index,1)[0]};Array.prototype.extend=function(array2){this.push.apply(this,array2)};Array.prototype.remove=function(item){var index;index=this.find(item);this.splice(index,1)};Array.prototype.copy=function(){return this.slice(0)};function dict(iterable){var result,key;result={};var _$rapyd$_Iter2=iterable;for(var _$rapyd$_Index2=0;_$rapyd$_Index2<_$rapyd$_Iter2.length;_$rapyd$_Index2++){key=_$rapyd$_Iter2[_$rapyd$_Index2];result[key]=iterable[key]}return result}if(typeof Object.getOwnPropertyNames!=="function"){dict.keys=function(hash){var keys;keys=[];
        for (var x in hash) {
            if (hash.hasOwnProperty(x)) {
                keys.push(x);
            }
        }
        ;return keys}}else{dict.keys=function(hash){return Object.getOwnPropertyNames(hash)}}dict.values=function(hash){var vals,key;vals=[];var _$rapyd$_Iter3=dict.keys(hash);for(var _$rapyd$_Index3=0;_$rapyd$_Index3<_$rapyd$_Iter3.length;_$rapyd$_Index3++){key=_$rapyd$_Iter3[_$rapyd$_Index3];vals.append(hash[key])}return vals};dict.items=function(hash){var items,key;items=[];var _$rapyd$_Iter4=dict.keys(hash);for(var _$rapyd$_Index4=0;_$rapyd$_Index4<_$rapyd$_Iter4.length;_$rapyd$_Index4++){key=_$rapyd$_Iter4[_$rapyd$_Index4];items.append([key,hash[key]])}return items};dict.copy=dict;dict.clear=function(hash){var key;var _$rapyd$_Iter5=dict.keys(hash);for(var _$rapyd$_Index5=0;_$rapyd$_Index5<_$rapyd$_Iter5.length;_$rapyd$_Index5++){key=_$rapyd$_Iter5[_$rapyd$_Index5];delete hash[key]}};dataFileName="data/Auckland_AUs_2013_with_rents.geojson";function makeMap(){var clon,clat,eps,map,tilesURL,BINS,LABELS,COLORS,MEDIAN_ANNUAL_INCOME,suburbs,info,legend,item;clon=174.73986;clat=-36.74041;eps=.8;map=L.map("map",{"center":[clat,clon],"zoom":9,"minZoom":9,"maxBounds":[[clat-eps,clon-eps],[clat+eps,clon+eps]]});tilesURL="http://{s}.tiles.mapbox.com/v3/github.map-xgq2svrz/{z}/{x}/{y}.png";map.attributionControl.setPrefix("");BINS=[0,.25,.5,.75,1e10];LABELS=["n/a","0&ndash;25%","26&ndash;50%","51&ndash;75%","76%+"];COLORS=reversed(["#d7191c","#fdae61","#abdda4","#2b83ba","#bbb"]);MEDIAN_ANNUAL_INCOME=882*52;suburbs=null;info=L.control();info.onAdd=function(map){this._div=L.DomUtil.create("div","info");this.update();return this._div};info.update=function(feature){if(typeof feature==="undefined")feature=null;var message;if(feature){message="<h4>"+feature.properties.AU_NAME+"</h4>"+"Weekly rent per bedroom: "+getWeeklyRent(feature,0,true)+"<br>"+"Fraction of annual income: "+getRentFraction(feature,2,true)+"<br>"}else{message="<h4>Suburb Info</h4>Hover over a suburb"}this._div.innerHTML=message};info.addTo(map);legend=L.control({position:"bottomright"});legend.onAdd=function(map){var div,i;div=L.DomUtil.create("div","info legend");var _$rapyd$_Iter6=reversed(range(len(LABELS)));for(var _$rapyd$_Index6=0;_$rapyd$_Index6<_$rapyd$_Iter6.length;_$rapyd$_Index6++){i=_$rapyd$_Iter6[_$rapyd$_Index6];div.innerHTML+='<i style="background:'+getColor(BINS[i])+'"></i> '+LABELS[i]+"<br>"}return div};legend.addTo(map);function getGrossAnnualIncome(string){if(typeof string==="undefined")string=false;var result;result=$("#income").val();if(!string){result=numToDollarStr(result,0,true)}return result}function getWeeklyRent(feature,ndigits,string){if(typeof ndigits==="undefined")ndigits=0;if(typeof string==="undefined")string=false;var numBedrooms,rent,result;numBedrooms=$("#num-bedrooms").val();if(feature.properties.rent_by_nbedrooms!="NA"){rent=parseFloat(feature.properties.rent_by_nbedrooms[numBedrooms]);if(numBedrooms=="5+"){result=rent/5}else{result=rent/numBedrooms}}else{result=-1}if(result>=0){if(string){result=numToDollarStr(result,ndigits,false)}}else{if(string){result="n/a"}else{result=-1}}return result}function getRentFraction(feature,ndigits,string){if(typeof ndigits==="undefined")ndigits=2;if(typeof string==="undefined")string=false;var result;result=52*getWeeklyRent(feature,ndigits,false)/getGrossAnnualIncome();if(result>=0){if(string){result=Math.ceil(result*100)+"%"}else{result=parseFloat(result.toFixed(ndigits))}}else{if(string){result="n/a"}}return result}function numToDollarStr(x,ndigits,inverse){if(typeof ndigits==="undefined")ndigits=0;if(typeof inverse==="undefined")inverse=false;var y,_$rapyd$_Unpack,cents,dollars;if(!inverse){y=x.toFixed(ndigits);_$rapyd$_Unpack=y.split(".");dollars=_$rapyd$_Unpack[0];cents=_$rapyd$_Unpack[1];dollars=dollars.replace(/\B(?=(\d{3})+(?!\d))/g,",");if(ndigits){return"$"+dollars+"."+cents}else{return"$"+dollars}}else{return parseInt(x.replace("$","").replace(",",""))}}function getColor(x){var _$rapyd$_Unpack,i,grade;var _$rapyd$_Iter7=enumerate(BINS);for(var _$rapyd$_Index7=0;_$rapyd$_Index7<_$rapyd$_Iter7.length;_$rapyd$_Index7++){_$rapyd$_Unpack=_$rapyd$_Iter7[_$rapyd$_Index7];i=_$rapyd$_Unpack[0];grade=_$rapyd$_Unpack[1];if(x<=grade){return COLORS[i]}}}function style(feature){var c;c=getColor(getRentFraction(feature));return{"fillColor":c,"fillOpacity":.7,"color":"white","weight":1,"opacity":1}}function highlightFeature(e){var layer;layer=e.target;layer.setStyle({"color":"black"});if(!L.Browser.ie&&!L.Browser.opera){layer.bringToFront()}info.update(layer.feature)}function resetHighlight(e){var layer;layer=e.target;suburbs.resetStyle(layer);info.update()}function zoomToFeature(e){map.fitBounds(e.target.getBounds())}function onEachFeature(feature,layer){layer.on({"mouseover":highlightFeature,"mouseout":resetHighlight,"click":zoomToFeature})}$.getJSON(dataFileName,function(collection){suburbs=L.geoJson(collection,{style:style,onEachFeature:onEachFeature}).addTo(map)});$(function(){var sv,min,range,el;$("#slider-vertical").slider({"orientation":"vertical","range":"min","min":100,"max":1e5,"value":MEDIAN_ANNUAL_INCOME,"step":100,"slide":function(event,ui){$("#income").val(numToDollarStr(ui.value));suburbs.setStyle(style)}});sv=$("#slider-vertical");$("#income").val(numToDollarStr(sv.slider("value")));min=sv.slider("option","min");range=sv.slider("option","max")-min;console.log("range=",range,MEDIAN_ANNUAL_INCOME/range*100);el=$('<label><span id="arrow">&larr;</span>'+"Median annual income<br>of employed Aucklanders<br>("+numToDollarStr(MEDIAN_ANNUAL_INCOME)+")</label>").css("bottom",MEDIAN_ANNUAL_INCOME/range*100+"%");$("#slider-vertical").append(el)});$(function(){$("#num-bedrooms").selectable({"selected":function(event,ui){$("#num-bedrooms").val(ui.selected.id);suburbs.setStyle(style)}})});item=$("#num-bedrooms li:eq(1)");item.addClass("ui-selected");$("#num-bedrooms").val(item[0].id)}makeMap()})();