// postman.js
// Copyright 2007-2013 cmonos.jp
// Last Modified:2012-05-16

var postman = {};
postman.window = {
	setOnLoad : function (func) {
		return postman.element._addEventListener(window,'load',func,false);
	},

	setOnUnload : function (func) {
		return postman.element._addEventListener(window,'unload',func,false);
	},

	setOnBeforeUnload : function (func) {
		return postman.element._addEventListener(window,'beforeunload',func,false);
	}
};

postman.value = {
	isIncluded : function(array,value) {
		if (array && array.constructor == Array) {
			for (var i=0; i < array.length; i++) {
				if (array[i] == value) return true;
			}
		}
		return false;
	},

	deleteFromArray : function (this_array,this_value) {
		var array = new Array();
		if (this_array) {
			for (var value in this_array) {
				if ((typeof this_array[value] == "string" || this_array[value] == "number") && this_array[value] != this_value) array.push(this_array[value]);
			}
		}
		return array;
	},

	escapeHTML : function (str) {
		var div = document.createElement('div');
		var text = document.createTextNode(str);
		div.appendChild(text);
		return div.innerHTML;
	},

	unescapeHTML : function (str) {
		return (str == null) ? '' : str.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&amp;/g,'&');
	},

	urlDecode : function (query) {
		var hash = new Array();
		if (query == null || query == "" || query.search("=") == -1) return hash;
		query = query.replace(/^\?/,'').split('&');
		for (var i=0; i<query.length; i++) {
			var p = query[i].split('=');
			if (window.decodeURIComponent) {
				p[0] = decodeURIComponent(p[0].replace(/\+/g,' '));
				p[1] = decodeURIComponent(p[1].replace(/\+/g,' '));
			} else {
				p[0] = unescape(p[0].replace(/\+/g,' '));
				p[1] = unescape(p[1].replace(/\+/g,' '));
			}
			if (hash[p[0]] == null) {
				hash[p[0]] = p[1];
			} else {
				if (hash[p[0]].constructor == Array) {
					hash[p[0]].push(p[1]);
				} else {
					hash[p[0]] = new Array(hash[p[0]],p[1]);
				}
			}
		}
		return hash;
	},

	urlEncode : function (hash,required_keys) {
		var query = '';
		for (var key in hash) {
			if (hash[key] != null && (required_keys == null || postman.value.isIncluded(required_keys,key))) {
				var encoded_key = ((window.encodeURIComponent) ? encodeURIComponent(key) : escape(key)).replace(/ /g,'+')
				if (hash[key].constructor == Array) {
					for (var i=0; i<hash[key].length; i++) {
						if ((typeof hash[key][i] == "string" || typeof hash[key][i] == "number") && hash[key][i] != null) query += ((query != "") ? "&" : "") + encoded_key + "=" + ((window.encodeURIComponent) ? encodeURIComponent(hash[key][i]) : escape(hash[key][i])).replace(/ /g,'+');
					}
				} else if (typeof hash[key] == "string" || typeof hash[key] == "number") {
					query += ((query != "") ? "&" : "") + encoded_key + "=" + ((window.encodeURIComponent) ? encodeURIComponent(hash[key]) : escape(hash[key])).replace(/ /g,'+');
				}
			}		
		}
		return query;
	},

	toHex : function (this_num) {
		this_num = eval(this_num);
		return ((this_num < 16) ? '0' : '') + this_num.toString(16)
	},

	comma : function (this_number) {
		this_number += "";
		var digit_number = '';
		var number_length = this_number.length;
		for (var i=3; i<number_length+3; i+=3) {
			if (digit_number != '') digit_number = ',' + digit_number;
			var start_point = -1 * i;
			var end_point = 3;
			if (i > number_length) {
				start_point = -1 * number_length;
				end_point = number_length + 3 - i;
			}
			digit_number = this_number.substr(start_point,end_point) + digit_number;
		}
		var check_number = digit_number.replace(/,/g,"");
		if (this_number == check_number) {
			return digit_number;
		} else {
			return this_number;
		}
	}
};

postman.element = {
	item : function(element) {
		if (arguments.length > 1) element = Array.prototype.slice.call(arguments);
		this.elements = new Array();
		return this.append(element);
	},

	form : function(element) {
		this.elements = new Array();
		if (typeof element == 'object') {
			this.currentForm = element;
		} if (typeof element == "string") {
			this.currentForm = document.getElementById(element);
		}
		return this;
	},

	fieldname : function(name,num) {
		if (typeof name == 'object') {
			if (!this.isIncluded(name)) this.elements[this.elements.length] = name;
		} else if (this.currentForm && typeof name == "string") {
			var n = 0;
			for (var i=0; i < this.currentForm.elements.length; i++) {
				if (this.currentForm.elements[i].name == name) {
					if ((!num || num == n) && (!this.isIncluded(this.currentForm.elements[i]))) this.elements[this.elements.length] = this.currentForm.elements[i];
					n++;
				}
			}
		}
		return this;
	},

	list : function () { return (this.elements) ? this.elements : [] },
	shift : function () { return (this.elements) ? this.elements.shift() : null },
	first : function () { return (this.elements) ? this.elements[0] : null },

	append : function(element) {
		if (arguments.length > 1) element = Array.prototype.slice.call(arguments);
		if (!element) return this;
		if (!this.elements) this.elements = new Array();
		if (element.constructor == Array) {
			for (var i=0; i<element.length; i++) {
				this.append(element[i]);
			}
		} else if (typeof element == 'object') {
			if (!this.isIncluded(element)) this.elements[this.elements.length] = element;
		} else if (typeof element == "string") {
			if (element.match(/^(\w+)\.([\w\-]+)$/)) {
				this.appendElementsByTagClass(RegExp.$1.toLowerCase(),RegExp.$2)
			} else {
				element = document.getElementById(element.replace('#',''));
				if (element && !this.isIncluded(element)) this.elements[this.elements.length] = element;
			}
		}
		return this;
	},

	isIncluded : function(value) {
		for (var i=0; i < this.elements.length; i++) {
			if (this.elements[i] == value) return true;
		}
		return false;
	},

	removeClassName : function(cName) {
		return this.replaceClassName(cName,'');
	},

	replaceClassName : function(cName,newName) {
		if (this.elements && cName != null && cName != "") {
			var regexp = new RegExp("(^|\\s)"+cName+"(?![\\w\\-])");
			if (newName == null) newName = '';
			for (var i=0; i < this.elements.length; i++) {
				if (this.elements[i].className != null) this.elements[i].className = this.elements[i].className.replace(regexp,newName);
			}
		}
		return this;
	},

	hasClassName : function(cName) {
		if (this.elements && cName != null && cName != "") {
			var regexp = new RegExp("(^|\\s)"+cName+"(?![\\w\\-])");
			for (var i=0; i < this.elements.length; i++) {
				if (this.elements[i].className == null || this.elements[i].className.search(regexp) == -1) return false;
			}
			return true;
		} else {
			return false;
		}
	},

	addClassName : function(cName) {
		if (this.elements && cName != null && cName != "") {
			var regexp = new RegExp("(^|\\s)"+cName+"(?![\\w\\-])");
			for (var i=0; i < this.elements.length; i++) {
				if (this.elements[i].className == null || this.elements[i].className == "") {
					this.elements[i].className = cName;
				} else if (this.elements[i].className.search(regexp) == -1) {
					this.elements[i].className += ' ' + cName;
				}
			}
		}
		return this;
	},

	changeClassName : function(cName,flag) {
		if ((flag == null || flag) && this.elements && cName != null && cName != "") {
			for (var i=0; i < this.elements.length; i++) {
				this.elements[i].className = cName;
			}
		}
		return this;
	},

	addEventListener : function(type,func,capture) {
		if (this.elements) {
			for (var i=0; i < this.elements.length; i++) {
				this._addEventListener(this.elements[i],type,func,capture);
			}
		}
		return this;
	},

	_addEventListener : function(element,type,func,capture) {
		if (capture == null) capture = false;
		if (typeof element.addEventListener =='function') {
			type = this.fixEventHandler(type);
			element.addEventListener(type, func, capture);
		} else if (typeof element.attachEvent == 'object') {
			element.attachEvent("on" + type, func);
		}
		return func;
	},

	fixEventHandler : function (type) {
		return (type == 'mousewheel' && typeof document.onmousewheel == 'undefined') ? 'DOMMouseScroll' : 
			(!('createTouch' in document)) ? type : 
			(type == 'mousedown') ? 'touchstart' : 
			(type == 'mousemove') ? 'touchmove' : 
			(type == 'mouseup') ? 'touchend' : 
			(type == 'mouseout') ? 'touchend' : 
			(type == 'mouseover') ? 'touchstart' : 
			(type == 'click') ? 'touchend' : 
			type;
	},

	removeEventListener : function(type,func,capture) {
		if (this.elements) {
			for (var i=0; i < this.elements.length; i++) {
				this._removeEventListener(this.elements[i],type,func,capture);
			}
		}
		return this;
	},

	_removeEventListener : function(element,type,func,capture) {
		if (capture == null) capture = false;
		if (typeof element.removeEventListener == 'function') {
			type = this.fixEventHandler(type);
			element.removeEventListener(type,func,capture);
		} else if (typeof element.detachEvent == 'object') {
			element.detachEvent("on" + type, func);
		}
		return func;
	},

	stopPropagation : function(e) {
		e = e || event || window.event;
		if (e.stopPropagation) {
			e.stopPropagation();
		} else {
			e.cancelBubble = true;
		}
		return this;
	},

	preventDefault : function (e) {
		e = e || event || window.event;
		if (e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}
		return this;
	},

	getProperty : function (e,k) {
		return (e.postman_property != null && e.postman_property[k] != null) ? e.postman_property[k] : null;
	},

	setProperty : function (e,k,v) {
		if (e.postman_property == null) e.postman_property = {};
		e.postman_property[k] = v; 
		return this;
	}
};

postman.form = {
	item : function(element) {
		if (typeof element == 'object') {
			this.currentForm = element;
		} else if (typeof element == "string") {
			this.currentForm = document.getElementById(element);
		} else {
			this.currentForm = null;
		}
		return this;
	},

	name : function (this_name) {
		for (var i=0; i<document.forms.length; i++) {
			if (document.forms[i].name == this_name) {
				this.currentForm = document.forms[i];
				return this;
			}
		}
		return this;
	},

	field : function(element) {
		if (typeof element == 'object') {
			this.currentField = element;
		} else if (typeof element == "string") {
			this.currentField = document.getElementById(element);
		} else {
			this.currentField = null;
		}
		return this;
	},

	fieldname : function(name,num) {
		if (typeof name == 'object') {
			this.currentField = name;
		} else if (typeof name == "string") {
			if (this.currentForm) {
				var n = 0;
				for (var i=0; i < this.currentForm.elements.length; i++) {
					if (this.currentForm.elements[i].name == name) {
						if (!num || num == n) {
							this.currentField = this.currentForm.elements[i];
							return this;
						}
						n++;
					}
				}
			} else {
				this.currentField = document.getElementById(name);
			}
		}
		return this;
	},

	getFieldsByName : function(name) {
		if (typeof name == 'object') {
			return new Array(name);
		} else if (typeof name == "string") {
			if (this.currentForm) {
				var list = new Array();
				for (var i=0; i < this.currentForm.elements.length; i++) {
					if (this.currentForm.elements[i].name == name) {
						list[list.length] = this.currentForm.elements[i];
					}
				}
				return list;
			} else {
				return new Array(document.getElementById(name));
			}
		}
		return this;
	},

	isTextField : function (type) {
		if (!type && this.currentField) type = this.currentField.type;
		return (postman.value.isIncluded([null,'','textarea','text','search','tel','url','email','password','datetime','date','month','week','time','datetime-local','number','range','color'],type.toLowerCase())) ? true : false;
	},

	getFieldProperty : function (k) {
		return (this.currentField) ? postman.element.getProperty(this.currentField,k) : null;
	},

	setFieldProperty : function (k,v) {
		if (this.currentField) postman.element.setProperty(this.currentField,k,v);
		return this;
	},

	getFormProperty : function (k) {
		return (this.currentForm) ? postman.element.getProperty(this.currentForm,k) : null;
	},

	setFormProperty : function (k,v) {
		if (this.currentForm) postman.element.setProperty(this.currentForm,k,v);
		return this;
	},

	getCurrentForm : function () { return this.currentForm || null; },
	getCurrentField : function () { return this.currentField || null; },

	setAutoFit : function () {
		if (!this.currentField) return true;
		var defaultHeight = this.getFieldProperty('defaultHeight');
		if (!defaultHeight) {
			defaultHeight = this.currentField.offsetHeight;
			this.setFieldProperty('defaultHeight',defaultHeight);
		}
		this.currentField.style.height = ((defaultHeight) ? defaultHeight : this.currentField.rows * 16) + 'px';
		(function (this_area) { postman.element.item(this_area).addEventListener('keyup', function () {
			if (this_area.scrollHeight > this_area.offsetHeight){
				this_area.style.height = this_area.scrollHeight + 30 + 'px';
			} else {
				while (this_area.scrollHeight - 50 < parseInt(this_area.style.height)) {
					var h = parseInt(this_area.style.height) - 50;
					if (h < 20) {
						this_area.style.height = '20px';
						break;
					} else {
						this_area.style.height = h + 'px';
					}
				}
				if (this_area.scrollHeight > this_area.offsetHeight) this_area.style.height = this_area.scrollHeight + 30 + 'px';
			}
			this_area.focus();
		}); })(this.currentField);
	},

	//選択肢補助
	proposalTextMenu : function(text) {
		if (this.currentField && text.constructor == Array) {
			var menu = this.createProposalTextMenu();
			for (var i=0; i<text.length; i++) {
				this.createProposalTextMenuOption(menu,text[i]);
			}
		}
	},
	proposalNumberMenu : function(max) {
		if (this.currentField && !isNaN(max) && max > 0) {
			var menu = this.createProposalTextMenu();
			for (var i=1; i<=max; i++) {
				this.createProposalTextMenuOption(menu,i);
			}
		}
	},
	createProposalTextMenu : function(text) {
		if (this.currentField) {
			var menu = this.getFieldProperty('proposalTexMenu');
			if (menu != null) return menu;
			menu = document.createElement('ul');
			document.getElementsByTagName('body')[0].appendChild(menu);
			menu.className = "proposal-text-menu";
			menu.style.width = this.currentField.offsetWidth + "px";
			menu.style.top = (postman.element.offsetTop(this.currentField) + this.currentField.offsetHeight) + "px";
			menu.style.left = postman.element.offsetLeft(this.currentField) + "px";
			this.setFieldProperty('proposalTextMenu',menu);
			return menu;
		}
	},
	createProposalTextMenuOption : function(menu,text) {
		var option = document.createElement('li');
		menu.appendChild(option);
		option.appendChild(document.createTextNode(text));
		var this_field = this.currentField;
		postman.element.item(option).addEventListener('click',function() {
			postman.form.field(this_field).setValue(option.innerHTML);
		});
	},
	clearProposalTextMenu : function() {
		if (this.currentField) {
			var menu = this.getFieldProperty('proposalTextMenu');
			if (menu != null) {
				this.setFieldProperty('proposalTextMenu',null);
				setTimeout(function() { document.getElementsByTagName('body')[0].removeChild(menu); },200);
			}
		}
	},


	//チェックボックス連動（複数）
	checkboxSync : function(this_checked,flag) {
		if (this.currentField && this.currentField.tagName.toLowerCase() == 'input' && (this.currentField.type.toLowerCase() == 'checkbox' || this.currentField.type.toLowerCase() == 'radio')) {
			if (flag == null) flag = true;
			if ((this_checked && flag) || (!this_checked && !flag)) {
				for (var i=2; i<arguments.length; i+=2) {
					postman.element.form(this.currentForm).fieldname(arguments[i]).shift().checked = arguments[i+1];
				}
			}
		}
	},
	checkboxSyncById : function() {
		for (var i=0; i<arguments.length; i+=2) {
			document.getElementById(arguments[i]).checked = arguments[i+1];
		}
	},

	//チェックまたは選択
	select : function(selected) {
		if (selected == null) selected = true;
		if (this.currentField.tagName.toLowerCase() == 'input' && (this.currentField.type.toLowerCase() == 'checkbox' || this.currentField.type.toLowerCase() == 'radio')) {
			this.currentField.checked = (selected) ? true : false;
		} else if (this.currentField.tagName.toLowerCase() == 'option') {
			this.currentField.selected = (selected) ? true : false;
		}
		return this;
	},

	//値
	getValue : function () {
		if (this.currentField == null) {
			return "";
		} else if (this.currentField.tagName.toLowerCase() == 'select') {
			return this.currentField.options[this.currentField.options.selectedIndex].value;
		} else if (this.currentField.tagName.toLowerCase() == 'input' && (this.currentField.type.toLowerCase() == 'checkbox' || this.currentField.type.toLowerCase() == 'radio')) {
			return (this.currentField.checked) ? this.currentField.value : "";
		} else if (this.currentField.value != null) {
			return this.currentField.value;
		}
		return "";
	},

	//一致するものだけ選択
	setValue : function(value) {
		if (this.currentField == null) return this;
		if (value == null) value = "";
		value += '';
		if (this.currentField.tagName.toLowerCase() == 'select') {
			for (var i=0; i < this.currentField.options.length; i++) {
				if (
					(value == "" && (this.currentField.options[i].value == null || this.currentField.options[i].value == "")) || 
					(value != "" && this.currentField.options[i].value != null && this.currentField.options[i].value != "" && this.currentField.options[i].value == value)
				) {
					this.currentField.options[i].selected = true;
				} else {
					this.currentField.options[i].selected = false;
				}
			}
		} else if (this.currentField.tagName.toLowerCase() == 'input' && (this.currentField.type.toLowerCase() == 'checkbox' || this.currentField.type.toLowerCase() == 'radio')) {
			this.currentField.checked = (this.currentField.value == value) ? true : false;
		} else {
			this.currentField.value = value;
		}
		return this;
	},

	//強調解除
	bailOut : function () {
		if (this.currentField) postman.validate.field(this.currentField).bailOut();
		return this;
	},

	//日付入力支援
	setDateFromDay : function (day,year_selector,mon_selector,mday_selector,hour_selector,min_selector,sec_selector) {
		var y = '';
		var m = '';
		var md = '';
		var h = '';
		var min = '';
		var sec = '';
		if (day != null && day != "") {
			day = eval(day);
			var this_date;
			if (isNaN(day)) day = 0;
			var this_date = new Date();
			this_date.setTime(86400000*day  + (new Date()).getTime());
			y = this_date.getFullYear();
			m = this_date.getMonth() + 1;
			md = this_date.getDate();
			h = this_date.getHours();
			min = this_date.getMinutes();
			sec = this_date.getSeconds();
		}
		if (year_selector != null && year_selector != "") this.fieldname(year_selector).setValue(y);
		if (mon_selector != null && mon_selector != "") this.fieldname(mon_selector).setValue(m);
		if (mday_selector != null && mday_selector != "") this.fieldname(mday_selector).setValue(md);
		if (hour_selector != null && hour_selector != "") this.fieldname(hour_selector).setValue(h);
		if (min_selector != null && min_selector != "") this.fieldname(min_selector).setValue(min);
		if (sec_selector != null && sec_selector != "") this.fieldname(sec_selector).setValue(sec);
	},

	//リセット
	reset : function () {
		if (this.currentField != null) {
			if (this.currentField.checked) {
				this.currentField.checked = false;
			} else if (this.currentField.options) {
				var done = false;
				for (var o=0; o < this.currentField.options.length; o++) {
					if (this.currentField.options[o].value == '') {
						this.currentField.options[o].selected = true;
						done = true;
					} else {
						this.currentField.options[o].selected = false;
					}
				}
			} else if (this.isTextField(this.currentField.type)) {
				this.currentField.value = '';
			} else if (this.currentField.type && this.currentField.type == 'file') {
				var id = this.currentField.id;
				if (id && document.getElementById(id+'-wrapper')) {
					var wrapper = document.getElementById(id+'-wrapper');
					var i = wrapper.innerHTML;
					wrapper.innerHTML = i;
				}
			} else if (this.currentField.type && this.currentField.type == 'textarea') {
				this.currentField.value = '';
			}
		}
	},
	resetAll : function (target_name) {
		for (var i=0; i < this.currentForm.elements.length; i++) {
			if (target_name == null || (this.currentForm.elements[i].name && this.currentForm.elements[i].name.search(target_name) != -1)) {
				this.field(this.currentForm.elements[i]).reset();
			}
		}
	},

	//連続投稿防止
	validate : function() {
		(function (this_form) { postman.element.item(this_form).addEventListener('submit',function(e) {
			var empty_fields = 0;
			for (var i=0; i<this_form.elements.length; i++) {
				var this_field = this_form.elements[i];
				if (postman.form.isTextField(this_field.type) && this_field.name.search(/^.+_=?$/) != -1) {
					if (this_field.value == null || this_field.value == "" || this_field.value.search(/\S/) == -1) {
						postman.validate.field(this_field).isInvalid();
						empty_fields++;
					}
				}
			}
			if (empty_fields > 0) {
				alert('いくつかの必須項目が入力されていません。');
				postman.element.stopPropagation(e);
				postman.element.preventDefault(e);
				return false;
			}
			var present_time = (new Date()).getTime();
			var submitted_time = postman.form.item(this_form).getFormProperty('submitted');
			if (submitted_time) {
				if ((present_time - submitted_time) > 30000) {
					if (confirm('既に送信されています。\nもう一度送信しますか？')) {
						postman.form.item(this_form).setFormProperty('submitted',present_time);
						return true;
					} else {
						postman.element.stopPropagation(e);
						postman.element.preventDefault(e);
						return false;
					}
				} else {
					alert('既に送信されています。\n新しい画面が読み込まれるまで、しばらくお待ちください。');
					postman.element.stopPropagation(e);
					postman.element.preventDefault(e);
					return false;
				}
			} else {
				postman.form.item(this_form).setFormProperty('submitted',present_time);
				return true;
			}
		}); })(this.currentForm);
	}
};

postman.validate = {
	field : function(element) {
		if (typeof element == 'object') {
			this.currentField = element;
		} else if (typeof element == "string") {
			this.currentField = document.getElementById(element);
		} else {
			this.currentField = null;
		}
		return this;
	},

	isInvalid : function () {
		if (this.currentField) postman.element.item(this.currentField).addClassName('invalid-field');
	},

	bailOut : function() {
		if (this.currentField) {
			postman.element.item(this.currentField).removeClassName('invalid-field');
			if (this.currentField.type && (this.currentField.type == 'checkbox' ||  this.currentField.type == 'radio')) {
				if (this.currentField.parentNode && this.currentField.parentNode.parentNode && this.currentField.parentNode.parentNode.tagName.toLowerCase() == 'li') {
					var this_list = this.currentField.parentNode.parentNode.parentNode;
					for (var i=0; i<this_list.childNodes.length; i++) {
						for (var n=0; n<this_list.childNodes[i].childNodes.length; n++){
							postman.element.item(this_list.childNodes[i].childNodes[n]).removeClassName('invalid-field');
						}
					}
				}
			}
		}
		return this;
	},

	//カラーチェック
	asColor : function(color,type) {
		if (color == null && this.currentField) color = this.currentField.value;
		if (type && type == 'rgb') color = color.replace(/^[\+\-]/,'');
		if (color == null || color =='' || color.search(/^#[0-9a-fA-F]{6}$/) != -1
			||	((!type && type == 'css') && (color.search(/^#[0-9a-fA-F]{3}$/) != -1 || color.search(/^(AliceBlue|AntiqueWhite|Aqua|Aquamarine|Azure|Beige|Bisque|Black|BlanchedAlmond|Blue|BlueViolet|Brown|BurlyWood|CadetBlue|Chartreuse|Chocolate|Coral|CornflowerBlue|Cornsilk|Crimson|Cyan|DarkBlue|DarkCyan|DarkGoldenRod|DarkGray|DarkGreen|DarkKhaki|DarkMagenta|DarkOliveGreen|Darkorange|DarkOrchid|DarkRed|DarkSalmon|DarkSeaGreen|DarkSlateBlue|DarkSlateGray|DarkTurquoise|DarkViolet|DeepPink|DeepSkyBlue|DimGray|DodgerBlue|FireBrick|FloralWhite|ForestGreen|Fuchsia|Gainsboro|GhostWhite|Gold|GoldenRod|Gray|Green|GreenYellow|HoneyDew|HotPink|IndianRed|Indigo|Ivory|Khaki|Lavender|LavenderBlush|LawnGreen|LemonChiffon|LightBlue|LightCoral|LightCyan|LightGoldenRodYellow|LightGrey|LightGreen|LightPink|LightSalmon|LightSeaGreen|LightSkyBlue|LightSlateGray|LightSteelBlue|LightYellow|Lime|LimeGreen|Linen|Magenta|Maroon|MediumAquaMarine|MediumBlue|MediumOrchid|MediumPurple|MediumSeaGreen|MediumSlateBlue|MediumSpringGreen|MediumTurquoise|MediumVioletRed|MidnightBlue|MintCream|MistyRose|Moccasin|NavajoWhite|Navy|OldLace|Olive|OliveDrab|Orange|OrangeRed|Orchid|PaleGoldenRod|PaleGreen|PaleTurquoise|PaleVioletRed|PapayaWhip|PeachPuff|Peru|Pink|Plum|PowderBlue|Purple|Red|RosyBrown|RoyalBlue|SaddleBrown|Salmon|SandyBrown|SeaGreen|SeaShell|Sienna|Silver|SkyBlue|SlateBlue|SlateGray|Snow|SpringGreen|SteelBlue|Tan|Teal|Thistle|Tomato|Turquoise|Violet|Wheat|White|WhiteSmoke|Yellow|YellowGreen)$/i) != -1))
			||	(type && type == 'html4' && color.search(/^(Black|Olive|Teal|Red|Blue|Maroon|Navy|Gray|Lime|Fuchsia|White|Green|Purple|Silver|Yellow|Aqua)$/i) != -1)
		) {
			if (this.currentField) {
				this.bailOut();
				this.currentField.style.backgroundColor = color;
				color.match(/^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})[0-9a-fA-F]{2}$/);
				if (eval("0x"+RegExp.$1) < 128 && eval("0x"+RegExp.$2) < 128) {
					this.currentField.style.color = '#FFF';
				} else {
					this.currentField.style.color = '#000';
				}
			}
			return true;
		} else {
			alert("色の形式を確認してください。");
			if (this.currentField) {
				this.isInvalid();
				this.currentField.focus(); 
				this.currentField.select(); 
				this.currentField.style.backgroundColor = "";
			}
			return false;
		}
	},

	//半角英数書式チェック
	asWord : function(str) {
		if (str == null && this.currentField) str = this.currentField.value;
		if (str && (str.search(/^[a-zA-Z0-9_]+$/) == -1)) {
			alert("半角英数字にしてください。");
			if (this.currentField) {
				this.isInvalid();
				this.currentField.focus(); 
				this.currentField.select(); 
			}
			return false;
		} else {
			this.bailOut();
			return true;
		}
	},

	//入力チェック
	asNotEmpty : function(str) {
		if (str == null && this.currentField) str = this.currentField.value;
		if (str == null || str == "" || str.search(/\S/) == -1) {
			alert("入力してください。");
			if (this.currentField) {
				this.isInvalid();
				this.currentField.focus(); 
				this.currentField.select(); 
			}
			return false;
		} else {
			this.bailOut();
			return true;
		}
	},

	//メールアドレス書式チェック
	asEMailAddress : function(email) {
		if (email == null && this.currentField) email = this.currentField.value;
		if (email && (email.search(/[0-9a-zA-Z_\+\-\.]+@[0-9a-zA-Z\-]+\.[0-9a-zA-Z\-\.]+/) == -1)) {
			alert("メールアドレスを確認してください。");
			if (this.currentField) {
				this.currentField.focus(); 
				this.currentField.select();
				this.isInvalid();
			}
			return false;
		} else {
			this.bailOut();
			return true;
		}
	},

	//URL書式チェック
	asUrl : function(url) {
		if (url == null && this.currentField) url = this.currentField.value;
		if (url && (url.search(/^https?:\/\/[0-9a-zA-Z\-]+\.[0-9a-zA-Z_~\-\.\/#\?\&=\%,]+$/) == -1)) {
			alert("URLを確認してください。");
			if (this.currentField) {
				this.isInvalid();
				this.currentField.focus(); 
				this.currentField.select();
			}
			return false;
		} else {
			this.bailOut();
			return true;
		}
	}
};

postman.validate.datetime = {
	gap : new Array(),

	fix : function(dt_type,sy,sm,sd,sh,smin,ey,em,ed,eh,emin) {
		if (this.gap[sy] == null || this.gap[sy] <= 0) this.gap[sy] = (sh == null || sh == "") ? 86400000 : 3600000; 
		var dt_start = this.getDateFromMenu(sy,sm,sd,sh,smin);
		var dt_start_time = dt_start.getTime();
		var dt_end = this.getDateFromMenu(ey,em,ed,eh,emin);
		var dt_end_time = dt_end.getTime();
		if (postman.form.field(sy).getValue() == "" && postman.form.field(sm).getValue() == "" && postman.form.field(sd).getValue() == "" && postman.form.field(sh).getValue() == "" && postman.form.field(smin).getValue() == "") {
			dt_start_time = dt_end_time - this.gap[sy];
			dt_start.setTime(dt_start_time);
		}
		if (postman.form.field(ey).getValue() == "" && postman.form.field(em).getValue() == "" && postman.form.field(ed).getValue() == "" && postman.form.field(eh).getValue() == "" && postman.form.field(emin).getValue() == "") {
			dt_end_time = dt_start_time + this.gap[sy];
			dt_end.setTime(dt_end_time);
		}
		if (parseInt(dt_start_time/60000) >= parseInt(dt_end_time/60000)) {
			if (dt_type == 'f') {
				dt_end_time = dt_start_time + this.gap[sy];
				dt_end.setTime(dt_end_time);
				this.setDateMenuByTime(dt_end,ey,em,ed,eh,emin);
			} else if (dt_type == 't') {
				dt_start_time = dt_end_time - this.gap[sy];
				dt_start.setTime(dt_start_time);
				this.setDateMenuByTime(dt_start,sy,sm,sd,sh,smin);
			}
		}
		this.gap[sy] = dt_end_time - dt_start_time;
		if (dt_type == 'f') {
			this.setDateMenuByTime(dt_start,sy,sm,sd,sh,smin);
		} else if (dt_type == 't') {
			this.setDateMenuByTime(dt_end,ey,em,ed,eh,emin);
		}
	},

	getDateFromMenu : function (y,m,d,h,min,date) {
		if (date == null) date = false;
		var md_done = false;
		var dt = new Date();
		if (y != null && y != "") {
			y = postman.form.field(y).getValue();
			if (!isNaN(y) && y >= 1970 && y < 2036) dt.setFullYear(parseInt(y));
		}
		if (m != null && m != "") {
			m = postman.form.field(m).getValue();
			if (!isNaN(m) && m >= 1 && m <= 12) {
				if (d != null && d != "") {
					d = postman.form.field(d).getValue();
					if (!isNaN(d) && d >= 1 && d <= 31) {
						dt.setMonth((parseInt(m) - 1),parseInt(d));
						md_done = true;
					}
				}
				if (!md_done) dt.setMonth(parseInt(m) - 1);
			}
		}
		if (!md_done && d != null && d != "") {
			d = postman.form.field(d).getValue();
			if (!isNaN(d) && d >= 1 && d <= 31) dt.setDate(parseInt(d));
		}
		if (h != null && h != "" && !date) {
			h = postman.form.field(h).getValue();
			dt.setHours((!isNaN(h) && h >= 0 && h < 24) ? parseInt(h) : 0);
		} else {
			dt.setHours(0);
		}
		if (min != null && min != "" && !date) {
			min = postman.form.field(min).getValue()
			dt.setMinutes((!isNaN(min) && min >= 0 && min < 60) ? parseInt(min) : 0);
		} else {
			dt.setMinutes(0);
		}
		dt.setSeconds(0);
		dt.setMilliseconds(0);
		return dt;
	},

	setDateMenuByTime : function (dt,y,m,d,h,min,date) {
		if (date == null) date = false;
		if (y != null && y != "" && !isNaN(dt.getFullYear())) postman.form.field(y).setValue(dt.getFullYear());
		if (m != null && m != "" && !isNaN(dt.getMonth())) postman.form.field(m).setValue((dt.getMonth() + 1));
		if (d != null && d != "" && !isNaN(dt.getDate())) postman.form.field(d).setValue(dt.getDate());
		if (h != null && h != "" && !isNaN(dt.getHours()) && !date) postman.form.field(h).setValue(dt.getHours());
		if (min != null && min != "" && !isNaN(dt.getMinutes()) && !date) postman.form.field(min).setValue(dt.getMinutes());
	}
};

postman.init = {
	document : function () {
		var this_init = this;
		postman.window.setOnLoad(function() {
			var is_mobile = (navigator.userAgent.search(/(android|iPhone|mobile)/i) != -1) ? true : false;
			var is_webkit = (navigator.userAgent.search(/webkit/i) != -1) ? true : false;
			var placeholder_enabled = (typeof (document.createElement('input')).placeholder == 'undefined') ? false : true;
			for (var n=0; n<document.forms.length; n++) {
				for (var i=0; i<document.forms[n].elements.length; i++) {
					var this_field = document.forms[n].elements[i];
					if (postman.form.isTextField(this_field.type)) {
						if (this_field.name.search(/^.+_=?$/) != -1) {
							(function (this_field) { postman.element.item(this_field).addEventListener('change',function() {
								postman.validate.field(this_field).asNotEmpty();
							}); })(this_field);
						}
						if (this_field.name.search(/_e[\!_]*$/) != -1) {
							(function (this_field) { postman.element.item(this_field).addEventListener('change',function() {
								postman.validate.field(this_field).asEMailAddress();
							}); })(this_field);
						}
						if (this_field.name.search(/_U[\!_]*$/) != -1) {
							(function (this_field) { postman.element.item(this_field).addEventListener('change',function() {
								postman.validate.field(this_field).asUrl();
							}); })(this_field);
						}
						if ((!placeholder_enabled || (is_webkit && this_field.type == 'textarea')) && typeof this_field.getAttribute('placeholder') != 'undefined' && typeof this_field.getAttribute('placeholder') != 'object' && this_field.getAttribute('placeholder') != null && this_field.getAttribute('placeholder') != "") {
							this_init.setPlaceholder(document.forms[n],this_field);
						}
						if (is_mobile) {
							if (this_field.type == 'textarea') postman.form.field(this_field).setAutoFit();
							this_field.style.maxWidth = "200px";
						}
					}
				}
				postman.form.item(document.forms[n]).validate();
			}
		});
		postman.window.setOnBeforeUnload(function() {
			this_init.hidePlaceholder();
		});
	},

	setPlaceholder : function (this_form,this_input) {
		if (this_input.value == null || this_input.value == "") {
			postman.element.item(this_input).addClassName('placeholder');
			this_input.value = this_input.getAttribute('placeholder');
		}
		postman.element.item(this_input).addEventListener('blur', function () {
			if (this_input.value == null || this_input.value == "") {
				postman.element.item(this_input).addClassName('placeholder');
				this_input.value = this_input.getAttribute('placeholder');
			}
		});
		postman.element.item(this_input).addEventListener('focus', function () {
			if (postman.element.item(this_input).hasClassName('placeholder')) {
				postman.element.item(this_input).removeClassName('placeholder');
				this_input.value = '';
			}
		});
		postman.element.item(this_form).addEventListener('submit', function () {
			for (var e=0; e<this_form.elements.length; e++) {
				var this_input = this_form.elements[e];
				if (postman.form.isTextField(this_input.type) && typeof this_input.getAttribute('placeholder') != 'undefined' && this_input.getAttribute('placeholder') != "" && postman.element.item(this_input).hasClassName('placeholder')) {
					this_input.value = '';
				}
			}
			return true;
		});
	},

	hidePlaceholder : function () {
		if (typeof (document.createElement('input')).placeholder == 'undefined') {
			for (var n=0; n<document.forms.length; n++) {
				for (var i=0; i<document.forms[n].elements.length; i++) {
					var this_input = document.forms[n].elements[i];
					if (postman.form.isTextField(this_input.type) && typeof this_input.getAttribute('placeholder') != 'undefined' && typeof this_input.getAttribute('placeholder') != 'object' && this_input.getAttribute('placeholder') != null && this_input.getAttribute('placeholder') != "" && postman.element.item(this_input).hasClassName('placeholder')) {
						this_input.value = '';
					}
				}
			}
		}
	}
};

postman.init.document();


