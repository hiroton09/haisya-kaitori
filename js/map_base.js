
function load() {
	if (GBrowserIsCompatible()) {
	
		//座標設定 
		var map = new GMap2(document.getElementById("mapData"));
		var lon   = 135.192915	; //経度
		var lat   = 34.227771	; //緯度
		var point = new GLatLng(lat, lon);
		
		//コントロール追加
		map.addControl(new GLargeMapControl());//ズームコントロール
		map.addControl(new GMapTypeControl());//航空写真とかを増やす
		map.addControl(new GScaleControl());//左下のスケール
		map.addControl(new GOverviewMapControl(new GSize(175,130)));//右下のちっさいやつ、数値が幅と高さ
		
		map.setCenter(point, 16); //ズームレベルの初期設定（1～19）数値が大きいほど拡大詳細表示がデフォルトになる
		
		
		//インフォウィンドウに入れる文字など、タグ挿入可、imgも入ります。'"はエスケープしておくこと！
		var textnode = '<dl><dt><img src=\"img/common/logo.gif\" alt=\"ペルソナビューティ倶楽部 PBCメゾン太田店\" /></dt><dd>和歌山市太田114-23<br />0120-76-2980</dd></dl>';
		
		var marker = createMarker(point,textnode) 
		map.addOverlay(marker);
		marker.openInfoWindowHtml(textnode);
	}
}
function createMarker(point,html) {
	var marker = new GMarker(point);
	GEvent.addListener(marker, "click", function() {
	marker.openInfoWindowHtml(html);
	});
	return marker;
}

