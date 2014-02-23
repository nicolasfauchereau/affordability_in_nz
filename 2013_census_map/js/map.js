(function(){function _$rapyd$_extends(child,parent){child.prototype=new parent;child.prototype.constructor=child}function reversed(arr){var tmp=[];for(var i=arr.length-1;i>=0;i--){tmp.push(arr[i])}return tmp}function range(start,stop,step){if(arguments.length<=1){stop=start||0;start=0}step=arguments[2]||1;var length=Math.max(Math.ceil((stop-start)/step),0);var idx=0;var range=new Array(length);while(idx<length){range[idx++]=start;start+=step}return range}function len(obj){if(obj instanceof Array||typeof obj==="string")return obj.length;else{var count=0;for(var i in obj){if(obj.hasOwnProperty(i))count++}return count}}function enumerate(item){var arr=[];for(var i=0;i<item.length;i++){arr[arr.length]=[i,item[i]]}return arr}var JSON,str,geoDataFile,rentDataFile,modeDataFile,rentByNbedroomsByAu,MIndexByAu,M,aus;JSON=JSON||{};if(!JSON.stringify){
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
        ;return keys}}else{dict.keys=function(hash){return Object.getOwnPropertyNames(hash)}}dict.values=function(hash){var vals,key;vals=[];var _$rapyd$_Iter3=dict.keys(hash);for(var _$rapyd$_Index3=0;_$rapyd$_Index3<_$rapyd$_Iter3.length;_$rapyd$_Index3++){key=_$rapyd$_Iter3[_$rapyd$_Index3];vals.append(hash[key])}return vals};dict.items=function(hash){var items,key;items=[];var _$rapyd$_Iter4=dict.keys(hash);for(var _$rapyd$_Index4=0;_$rapyd$_Index4<_$rapyd$_Iter4.length;_$rapyd$_Index4++){key=_$rapyd$_Iter4[_$rapyd$_Index4];items.append([key,hash[key]])}return items};dict.copy=dict;dict.clear=function(hash){var key;var _$rapyd$_Iter5=dict.keys(hash);for(var _$rapyd$_Index5=0;_$rapyd$_Index5<_$rapyd$_Iter5.length;_$rapyd$_Index5++){key=_$rapyd$_Iter5[_$rapyd$_Index5];delete hash[key]}};geoDataFile="data/auckland_aus_2013.geojson";rentDataFile="data/mean_rents_by_nbedrooms_by_au.json";modeDataFile="data/distance_and_time_matrix.json";function numToDollarStr(x,inverse){if(typeof inverse==="undefined")inverse=false;var dollars;if(!inverse){if(x===null){return"n/a"}dollars=x.toFixed(0);dollars=dollars.replace(/\B(?=(\d{3})+(?!\d))/g,",");return"$"+dollars}else{if(x=="n/a"){return null}return parseInt(x.replace("$","").replace(",",""))}}rentByNbedroomsByAu=null;MIndexByAu=null;M=null;aus=null;$.getJSON(rentDataFile,function(data){rentByNbedroomsByAu=data});$.getJSON(modeDataFile,function(data){MIndexByAu=data["index_by_name"];M=data["matrix"]});$.getJSON(geoDataFile,function(data){aus=data;makeMap()});function makeMap(){var item,PARKING_DEFAULT,clon,clat,map,tilesURL,BINS,LABELS,COLORS,MEDIAN_ANNUAL_INCOME,COMMUTE_COST_PER_KM_PER_MODE,WEEKLY_FIXED_COST_PER_MODE,legend,workplace;MEDIAN_ANNUAL_INCOME=52*882;$(function(){var sv,min,range,el;$("#income-slider").slider({"orientation":"horizontal","range":"min","min":100,"max":1e5,"value":MEDIAN_ANNUAL_INCOME,"step":100,"slide":function(event,ui){$("#income").val(numToDollarStr(ui.value));aus.setStyle(style)}});sv=$("#income-slider");$("#income").val(numToDollarStr(sv.slider("value")));min=sv.slider("option","min");range=sv.slider("option","max")-min;el=$("<label>&#9650;</label><br>").css("left",MEDIAN_ANNUAL_INCOME/range*100+"%");$("#income-slider").append(el)});$(function(){$("#num-bedrooms").selectable({"selected":function(event,ui){$("#num-bedrooms").val(ui.selected.id);aus.setStyle(style)}})});item=$("#num-bedrooms li:eq(1)");item.addClass("ui-selected");$("#num-bedrooms").val(item[0].id);$(function(){$("#mode").selectable({"selected":function(event,ui){$("#mode").val(ui.selected.id);aus.setStyle(style)}})});item=$("#mode li:eq(1)");item.addClass("ui-selected");$("#mode").val(item[0].id);PARKING_DEFAULT=0;$(function(){var sv,min,range;$("#parking-cost-slider").slider({"orientation":"horizontal","range":"min","min":0,"max":20,"value":PARKING_DEFAULT,"step":1,"slide":function(event,ui){$("#parking").val(numToDollarStr(ui.value));aus.setStyle(style)}});sv=$("#parking-cost-slider");$("#parking").val(numToDollarStr(sv.slider("value")));min=sv.slider("option","min");range=sv.slider("option","max")-min});clon=174.739869;clat=-36.840417;map=L.map("map",{"center":[clat,clon],"zoom":10,"minZoom":8,"maxZoom":13,"maxBounds":[[clat-.8,clon-.8],[clat+.8,clon+1.1]]});tilesURL="http://{s}.tiles.mapbox.com/v3/github.map-xgq2svrz/{z}/{x}/{y}.png";map.attributionControl.setPrefix("");BINS=[0,.25,.5,.75,1e10];LABELS=["n/a","0&ndash;25%","26&ndash;50%","51&ndash;75%","76%+"];COLORS=reversed(["#d7191c","#fdae61","#abdda4","#2b83ba","#ccc"]);MEDIAN_ANNUAL_INCOME=882*52;COMMUTE_COST_PER_KM_PER_MODE={"walk":0,"bicycle":0,"car":.274,"bus":.218};WEEKLY_FIXED_COST_PER_MODE={"walk":0,"bicycle":500/52,"car":2228/52,"bus":0};legend=L.control({position:"bottomright"});legend.onAdd=function(map){var div,i;div=L.DomUtil.create("div","legend");div.innerHTML="<h4>Cost as<br/>% of income</h4>";var _$rapyd$_Iter6=reversed(range(len(LABELS)));for(var _$rapyd$_Index6=0;_$rapyd$_Index6<_$rapyd$_Iter6.length;_$rapyd$_Index6++){i=_$rapyd$_Iter6[_$rapyd$_Index6];div.innerHTML+='<i style="background:'+getColor(BINS[i])+'"></i> '+LABELS[i]+"<br>"}return div};legend.addTo(map);workplace=L.marker([-36.85119,174.76827],{"draggable":true}).addTo(map);workplace.bindPopup("Move this marker to where you work");workplace.on("dragend",function(e){setWorkplacePopup(this);aus.setStyle(style)});function getWorkplaceAuName(marker){var position,layer,auName;position=marker.getLatLng();try{layer=leafletPip.pointInLayer(position,aus,true)[0]}catch(_$rapyd$_Exception){console.log("Fail on pip");return null}if(layer){auName=layer.feature.properties.AU_NAME}else{auName=null}return auName}function setWorkplacePopup(marker){var auName,text;auName=getWorkplaceAuName(marker);text="<h4>Workplace</h4>";if(auName){text+=auName}else{text+="Undefined"}marker.setPopupContent(text);marker.openPopup()}aus=L.geoJson(aus,{"style":style,"onEachFeature":onEachFeature}).addTo(map);function getColor(x){var _$rapyd$_Unpack,i,grade;var _$rapyd$_Iter7=enumerate(BINS);for(var _$rapyd$_Index7=0;_$rapyd$_Index7<_$rapyd$_Iter7.length;_$rapyd$_Index7++){_$rapyd$_Unpack=_$rapyd$_Iter7[_$rapyd$_Index7];i=_$rapyd$_Unpack[0];grade=_$rapyd$_Unpack[1];if(x<=grade){return COLORS[i]}}return COLORS[0]}function style(feature){var c;c=getColor(getWeeklyTotalCostFraction(feature));return{"fillColor":c,"fillOpacity":.7,"color":"white","weight":1,"opacity":1}}function highlightFeature(e){var layer,feature,wtcf,_$rapyd$_Unpack,wcc,wct,popupContent;layer=e.target;feature=layer.feature;layer.setStyle({"color":"black"});if(!L.Browser.ie&&!L.Browser.opera){layer.bringToFront()}if(getWeeklyTotalCostFraction(feature)===null){wtcf="n/a"}else{wtcf=(getWeeklyTotalCostFraction(feature)*100).toFixed(0)+"%"}_$rapyd$_Unpack=getWeeklyCommuteCostAndTime(feature);wcc=_$rapyd$_Unpack[0];wct=_$rapyd$_Unpack[1];popupContent="<h4>"+feature.properties.AU_NAME+"</h4>"+"<table>"+"<tr><td>Weekly rent per bedroom</td><td>"+numToDollarStr(getWeeklyRent(feature),false)+"</td></tr>"+"<tr><td>Weekly commute cost</td><td>"+numToDollarStr(wcc,false)+"</td></tr>"+"<tr><td>Weekly commute time</td><td>"+wct.toFixed(1)+" h </td></tr>"+"<tr><td>Weekly parking cost</td><td>"+numToDollarStr(getWeeklyParkingCost(),false)+"</td></tr>"+"<tr><td>Total weekly cost</td><td>"+numToDollarStr(getWeeklyTotalCost(feature),false)+"</td></tr>"+"<tr><td>Fraction of annual income</td><td>"+wtcf+"</td></tr>"+"</table>";layer.bindPopup(popupContent,{"offset":L.point(0,220),"closeButton":false}).openPopup()}function resetHighlight(e){var layer;layer=e.target;aus.resetStyle(layer);layer._map.closePopup()}function zoomToFeature(e){map.fitBounds(e.target.getBounds())}function onEachFeature(feature,layer){layer.on({"mouseover":highlightFeature,"mouseout":resetHighlight,"click":zoomToFeature})}function getWeeklyIncome(){var income;income=$("#income").val();return numToDollarStr(income,true)/52}function getWeeklyRent(feature){var numBedrooms,auName,rent,result;numBedrooms=$("#num-bedrooms").val();auName=feature.properties.AU_NAME;if(rentByNbedroomsByAu[auName]=="NA"){result=null}else{rent=parseFloat(rentByNbedroomsByAu[auName][numBedrooms]);if(numBedrooms=="5+"){result=rent/5}else{result=rent/numBedrooms}}return result}function getWeeklyCommuteCostAndTime(feature){var mode,auName,i,workplaceAuName,j,_$rapyd$_Unpack,distance,time,cost;mode=$("#mode").val();auName=feature.properties.AU_NAME;i=MIndexByAu[auName];workplaceAuName=getWorkplaceAuName(workplace);if(workplaceAuName===null){console.log("Workplace AU name is None");return[0,0]}j=MIndexByAu[workplaceAuName];_$rapyd$_Unpack=M[mode][i][j];distance=_$rapyd$_Unpack[0];time=_$rapyd$_Unpack[1];cost=distance*10*COMMUTE_COST_PER_KM_PER_MODE[mode]+WEEKLY_FIXED_COST_PER_MODE[mode];return[cost,time*10]}function getWeeklyParkingCost(){var parking;parking=$("#parking").val();return numToDollarStr(parking,true)*7}function getWeeklyTotalCost(feature){var rent,total;rent=getWeeklyRent(feature);if(rent!==null){total=rent+getWeeklyCommuteCostAndTime(feature)[0]+getWeeklyParkingCost()}else{total=null}return total}function getWeeklyTotalCostFraction(feature){var total,fraction;total=getWeeklyTotalCost(feature);if(total!==null){fraction=total/getWeeklyIncome()}else{fraction=null}return fraction}}})();