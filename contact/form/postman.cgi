#!/usr/bin/perl
# サーバのパスに合わせる
use strict;
use utf8;
#use KCatch qw( mode=html );
use lib "./lib";
binmode STDOUT, ":utf8";

##################################################################################################################
# Copyright (C) 1999-2013 CMONOS (ENDO chihiro)
# POSTMAN ver3.0.4  postman.cgi
#
# 最終更新日：2013-01-10
##################################################################################################################
# 使い方：		入力欄の名前が"_"で始まる値はメールヘッダになります。
#					_To				宛先アドレス
#					_From			差出人アドレス
#					_Subject		表題
#
#					※メール送信時には「差出人アドレス：○○」等の形にされます。
#					　名前を変えたいときは"_○○"とします。
#					例）_From_送信者			差出人アドレス
#
# 				入力欄の名前が"_"で終わる値は入力が強制されます。
#					例）	コメント_	
#
# 				入力欄の名前が"!"で終わる値は、同じ名前の項目が全て同じ文字列かどうかチェックします。
#					例）	パスワード_P!	
#
# 				形式のチェック
# 				入力欄の名前が次の文字列で終わる値は、形式をチェックします。
# 					_E		E-Mail のチェック（複数のアドレス）
# 					_e		E-Mail のチェック
# 					_A		半角英数字（半角英数字 _ 半角空白 , . -）のチェック
# 					_a		半角英数字のチェック
# 					_N		半角数字のチェック
# 					_n		半角数字のチェック（計算結果に変換）
# 					_U		URLのチェック
# 					_p		半角英数字文字列かどうかチェック
# 					_P		半角英数字で始まる半角英数字文字列かどうかチェック
# 								_P-4-8	4文字以上8文字以下のパスワード
# 					_K		カタカナのチェック
# 					_H		ひらがなのチェック
#
#					例1）	ホームページ_U			URL チェック
#					例2）	メールアドレス_E_		入力の強制 + E-Mail チェック	
#
# 				データの順番を指定するときは冒頭に数字と_を加えます。
# 				※	通常はデータが送られてきた順になります。
# 				※	順番指定のあるデータと指定のないデータが混在している場合、
# 					指定のないデータの順序が乱れることがあります。
#					例）	01_名前			一つ目のデータ
#							02_コメント		二つ目のデータ
#
# 				"_THANKS"で送信後に表示するページを指定できます。
# 				※この指定がない場合、THANKSページを書き出します。
#					例）	<input type="hidden" name="_THANKS" value="URL">
#						!!URL			直接移動する
#
#					場合分けする例）<input type="hidden" name="_THANKS" value="変数名==値==URL||変数名==値==URL">
#						変数名==値==URL	変数名が値と一致するときURLを表示する
#						||				条件区切り。条件は順番に評価されます。
#
# 				"_DATA"でメールへの送信方法を指定できます。
#					例）	<input type="hidden" name="_DATA" value="csv">
#					csv	送信をCSV形式の添付ファイルに変換する。
#					tsv	送信をタブ区切りテキストの添付ファイルに変換する。
#					_		メッセージにもデータを含める。（csv_）
#
# 				"_ID"で登録番号を自動発行できます。
# 				※「会員番号」という名前で発行したいときは、"_ID_会員番号"とします。
# 				※識別記号を付けたい場合は、"_ID-A_会員番号"とします。→例）01234A
#					例）	<input type="hidden" name="_ID" value="番号保存ファイル名">
#							番号保存ファイル名は他のフォームと重複しないユニークな半角英字名にしてください。
#
# 				"_MSG"でメールの自動返信を設定できます
# 				※メールヘッダ"From"に対応する入力欄が必要です。
# 				※メールのタイトルを指定する場合、"_MSG_メールタイトル"とします。
# 				※返信文中の次のタグは自動変換されます。
#					<ID>			→	登録番号
#					<PASSWORD>		→	パスワード（最後のパスワード項目）
#					<DATA>			→	送信データのリスト
#					<EMAIL>			→	送信先アドレス
#					<MASTER_EMAIL>	→	CGI 管理者アドレス
#
#					例）	<input type="hidden" name="_MSG_登録ありがとうございます" value="返信文ファイル名">
#							あらかじめ、返信文ファイルを作成し、初期設定で指定したパスに設置してください。
#							返信文ファイル名は他のフォームと重複しないユニークな半角英字名にしてください。
#
#					場合分けする例）<input type="hidden" name="_MSG" value="変数名==値==返信文ファイル名||変数名==値==返信文ファイル名">
#						変数名==値==返信文ファイル名	変数名が値と一致するときURLを表示する
#						||								条件区切り。条件は順番に評価されます。
#						ファイルごとに表題を設定するには一行めに、「Subject:メールの表題[改行]」を入れます。
#
# 				"_HERE" でフォームのあるページを明示的に指定することが出来ます。
# 				※このオプションはリンク元を送信しない環境で動作させるためには必須です。
#					例）	<input type="hidden" name="_HERE" value="絶対パス">
#
# 				"_CONFIRMATION" で送信内容確認ページを経由させることが出来ます。
# 				※このオプションは最後のページに記述します。
#					例）	<input type="hidden" name="_CONFIRMATION" value="true">
#
# 				"_CONFIRMATIONPAGE" で送信内容確認ページを指定することが出来ます。
# 				※このオプションは最後のページに記述します。
#					例）	<input type="hidden" name="_CONFIRMATIONPAGE" value="./confirmation.html">
#						<!--FORM_ONLY--> ... <!--/FORM_ONLY-->			→	フォームでのみ表示する領域
#						<!--CONFIRMATION: ... -->						→	確認画面でのみ表示
#						<!--FIELD:変数名--> ... <!--/FIELD-->			→	対応するフィールドの値に置き換えます。
#
# 				"_NEXT" "_NEXTPAGE" "_PREV" "_PREVPAGE" で複数ページにわたる入力ページを作成できます。
#					例）	<input type="hidden" name="_PREVPAGE" value="./form.html">
#							<input type="submit" name="_PREV" value="前のページ">
#							<input type="hidden" name="_NEXTPAGE" value="./form2.html">
#							<input type="submit" name="_NEXT" value="次のページ">
#
# 				"_NOCHECK" でフォーマットチェックをスキップできます（入力ページが複数の場合）。
#					例）	<input type="hidden" name="_NOCHECK" value="true">
#
# 				"_DATE" で登録日時を送信できます。
#					例）	<input type="hidden" name="_DATE" value="/24">
#						'-'		->	'2005-11-25 13:23:55'
#						'v'		->	'2005/15/25T13:23:55Z'
#						'/'		->	'2005/11/25/(金) 1:23:55 p.m.'
#						'/24'	->	'2005/11/25/(金) 13:23:55'
#						'c'		->	'2005年11月25日(金) 午後1時23分55秒'
#						'c24'	->	'2005年11月25日(金) 13時23分55秒'
#						'cj'	->	'平成17年11月25日(金) 午後1時23分55秒'
#						'c24j'	->	'平成17年11月25日(金) 13時23分55秒'
#						'cjk'	->	'平成一七年一一月二五日(金) 午後一時二三分五五秒'
#						'c24jk'	->	'平成一七年一一月二五日(金) 一三時二三分五五秒'
#						'cJk'	->	'平成一七年霜月二五日(金) 午後一時二三分五五秒'
#						'c24Jk'	->	'平成一七年霜月二五日(金) 一三時二三分五五秒'
#
#				※FORM METHODは"POST"でなければなりません。
#				※チェックボックス対策
#					チェックボックスはチェックされていないと値が送られません。
#					hiddenを使って値の存在を明示することができます。値が"*"の場合無視されます。 
#					例）	<input type="hidden" name="チェックボックスと同じ名前" value="*">
#				※文字コードのヒント
#					下記を <form> の直後に入れておくと文字化けしにくくなります。値は全角の下線。
#					例）	<input type="hidden" name="_" value="＿">
#
# タグ例：		<input type="text" size="16" name="_From">
#					↓
#				入力された値がメールヘッダの差出人になります。
#
# 特殊な記法：	name 属性に URL エンコードされた値の組を設定することができます。
#
# 特殊な例1：	<input type="submit" name="_THANKS=/download1.html" value="ダウンロードページ1" />
# 				<input type="submit" name="_THANKS=/download2.html" value="ダウンロードページ2" />
#					↓
#				押すボタンによって表示されるお礼ページを変える場合。
#
# 特殊な例2：	<input type="submit" name="name=value&name2=value2" value="1" />
#					↓
#				一つのチェックボックスに複数の値を持たせる場合（value は無視されます）。
#
##################################################################################################################
# ［初期設定］
# メール送信方法の設定
# sendmailのパス or SMTPサーバのIPアドレス
my $sendmail = '/usr/sbin/sendmail';

# 管理者メールアドレス
my $cgi_master = 'info@haisha-kaitori.com';

# メール送信先の設定
# 宛先指定ヘッダを許可するかどうか（1=許可/0=禁止）
my $send_ok = 0;

# メール送信先（下記アドレスには必ず送信されます）[複数の場合はカンマで区切る]
my $mail_to = 'info@haisha-kaitori.com';

# メール送信先（Cc）[複数の場合はカンマで区切る]
my $mail_cc = '';

# メール送信先（Bcc）[複数の場合はカンマで区切る]
my $mail_bcc = 'sugano@enzine.jp';

# 直前URLを制限する（1=制限する/0=制限しない）
my $ref_check = 1;

# 直前URLの限定（以下にマッチしない場合$jump_toにジャンプします）
my $ref_uri = '';

# 直前URLが不正であったときの移動先
my $jump_to = 'http://www.google.co.jp/';

# 受け付けるファイルの拡張子
my @allowed_file_types = ('jpg','jpeg','gif','png','txt','csv','zip');

# 添付ファイルのファイルサイズ上限値（単位=バイト/1KB=1000）
my $sizelimit = 128000;

# 送信されたデータを添付ファイルに変換する
#		csv	送信をCSV形式の添付ファイルに変換する。
#		tsv	送信をタブ区切りテキストの添付ファイルに変換する。
#		_		メッセージにもデータを含める。（csv_）
my $sv = '';

# 登録番号保存ディレクトリ
my $number_dir = './data/number';

# 返信メール文書保存ディレクトリ
my $msg_dir = './data/msg';

########################################################################
# 環境
{
no warnings qw(once);

# ファイルのパーミッション
$env::file_mode = 0604;

# ディレクトリのパーミッション
$env::dir_mode = 0705;

# 一時保存ファイルディレクトリの位置（CGIから見た相対パス）
$env::clipboard = './data/clipboard';

# ブラウザからアクセス可能な一時保存ファイルディレクトリの位置（CGIから見た相対パス）
$env::public_clipboard = './clipboard';

# ファイルアップロード最大容量
$env::post_max_size = 100000000;

}
########################################################################
$mail_to = $cgi_master if !defined $mail_to || !$mail_to;
#オブジェクト
require CMONOS::CGI_Lib::Common;
my $input = Common->new ;
my $this = {};
bless $this;

#不正なアクセスははねる。
$input->referer_is_matched($ref_uri,$jump_to,1) if defined $ref_check && $ref_check;

#GETははねる。
$input->error404 if $ENV{'REQUEST_METHOD'} !~ /^POST$/i;

my(%input,%in,$referer,$files,$thanks_page,$thanks_page_jump,$message,$number,%count,%mail_header,@files,$mail,$user_name,
$action,$nextpage,$id,$id_name,$id_file,$id_ext,$msg,$msg_title,$msg_file,
$header,$to,$from,@error,@header,@data,%data,$passwd,%passwords,$no_check,@delete_files,@invalid_fields);
$no_check = 0;
$user_name = $number = $id_name = $id_file = $msg_file = $passwd = $message = $action = '';

#デコード
%input = $input->decode(0,'utf8','lf');
%in = $input->dename(\%input,'utf8','lf',$input->{'query_order'});
delete $input{''};
delete $in{''};

#呼び出し元ファイル
$referer = $ENV{'HTTP_REFERER'};
$referer =~ s/[#\?].*$//;
$referer .= 'index.html' if $referer =~ m!/$!;
if ($referer !~ /\.s?html?$/i) {
	$referer = '';
	$referer = $in{'_HERE'} if defined $in{'_HERE'} && $in{'_HERE'} =~ /\.s?html?$/i;
	$referer = $in{'_REFERER'} if defined $in{'_REFERER'} && $in{'_REFERER'} =~ /\.s?html?$/i;
}
delete $in{'_REFERER'};
delete $input{'_REFERER'};

if ($in{'_DELETE'}) {
	@delete_files = split(/\0/,$in{'_DELETE'});
	delete $in{'_DELETE'};
}
if ($in{'_CLIPBOARD'}) {
	$main::clipboard_id = $in{'_CLIPBOARD'};
	delete $input{'_CLIPBOARD'};
	delete $in{'_CLIPBOARD'};
}

#キャンセル
if (defined $in{'_CANCEL'} && $in{'_CANCEL'} ne '') {
	if ($main::clipboard_id) {
		foreach my $k (@{$input->{'query_order'}}) {
			$input->inherit_posted_file_properties($k);
		}
	}
	$this->print_form_page($input,$referer,\%input);
}

#移動する場合
if ($in{'_NEXT'} || $in{'_PREV'} || $in{'_CONFIRMATION'} || $in{'_CONFIRMATIONPAGE'}) {

	#次のページ
	if (defined $in{'_NEXT'} && $in{'_NEXT'} ne '') {
		$no_check = 1 if defined $in{'_NOCHECK'} && $in{'_NOCHECK'};
		$action = 'P';
		$nextpage = $input->path_change($in{'_NEXTPAGE'},$referer,'abs');

	#前のページ
	} elsif (defined $in{'_PREV'} && $in{'_PREV'} ne '') {
		$no_check = 1 if defined $in{'_NOCHECK'} && $in{'_NOCHECK'};
		$action = 'P';
		$nextpage = $input->path_change($in{'_PREVPAGE'},$referer,'abs');

	#確認画面
	} elsif ((defined $in{'_CONFIRMATION'} && $in{'_CONFIRMATION'} ne '') || (defined $in{'_CONFIRMATIONPAGE'} && $in{'_CONFIRMATIONPAGE'} ne '')) {
		$action = 'C';
		$nextpage = $input->path_change($in{'_CONFIRMATIONPAGE'},$referer,'abs') if defined $in{'_CONFIRMATIONPAGE'} && $in{'_CONFIRMATIONPAGE'};
		delete $in{'_CONFIRMATION'};
		delete $in{'_CONFIRMATIONPAGE'};
	}

	delete $in{'_NEXT'};
	delete $in{'_NEXTPAGE'};
	delete $in{'_PREV'};
	delete $in{'_PREVPAGE'};
}

#入力解析
no warnings qw(numeric);
$mail_header{'To'} = $mail_to;
$mail_header{'Cc'} = $mail_cc;
$mail_header{'Bcc'} = $mail_bcc;
$to = 'To|Cc|Bcc';
$from = 'From|Reply\-To';
foreach my $k (sort {
	my $da = ($a =~ /^(\d+)_/) ? $1 : '';
	my $db = ($b =~ /^(\d+)_/) ? $1 : '';
	$da <=> $db;
} @{$input->{'query_order'}}) {
	my($required,$check,$format,$is_invalid,$skip,$v,$offset,$limit,$key) = (0,0,'',0,0,'',0,0,'');
	next unless defined $in{$k};
	next if $count{$k}++;
	$v = $in{$k};
	$key = $k;
	$check = 1 if $k =~ s/\!(_?)$/$1/s;
	$required = 1 if $k =~ s/_(\!?)$/$1/s;

	#形式チェック
	if ($k =~ s/_([AaEeNnUPpKH])$//s) {
		$format = $1;
	} elsif ($k =~ s/_([Pp])(-(\d+))(-(\d+)|)$//s) {
		$format = $1;
		$offset = $3;
		$limit = $5;
	}

	$k =~ s/^\d+_(.+)$/$1/;
	$v = join("\0",grep($_ ne '*',split(/\0/,$v,-1)));
	$v = '' if $v =~ /^[\s\0]+$/;

	#添付ファイル
	if (grep($_ eq $key,@delete_files)) {
		$v = '';
	} elsif ($main::clipboard_id) {
		$input->inherit_posted_file_properties($key);
	}
	my @file_num = $input->get_posted_file_numbers($key);
	if (@file_num) {
		push(@files,'<' . $key . '>');
		if ($k =~ /^(?:_FILE_|)(.*)$/i) {
			$k = $1;
		} else {
			$k = '添付ファイル';
		}
		my @file_names;
		foreach my $num (@file_num) {
			my %properties = $input->get_posted_file_properties_from_param($key,$num);
			if (!$properties{'filename'} || !grep($properties{'filename'} =~ /\.$_$/i,@allowed_file_types)) {
				push(@error,$k . 'は許可されていない種類のファイルです。');
				$is_invalid = 1;
			} else {
				my $file_size = $input->get_posted_file_size_from_param($key,$num);
				if (defined $sizelimit && $sizelimit && $sizelimit > 0 && $file_size > $sizelimit) {
					push(@error,$k . 'のサイズが大きすぎます。\n' . $input->digit($sizelimit) . ' byte 以内にしてください。');
					$is_invalid = 1;
				} else {
					push(@file_names,$properties{'filename'});
				}
			}
			if ($is_invalid) {
				$input->remove_posted_file($key,$num);
			}
		}
		$v = (@file_names) ? join("\0",@file_names) : '';

	#登録日時
	} elsif ($k =~ s/^_DATE_?//) {
		$k = ($k) ? $k : '登録日時';
		$v = $input->date(0,$v);

	#移動先
	} elsif ($k =~ /^_THANKS$/) {
		$v = $1 if $v =~ /^(.*?)\0/;
		$thanks_page = $v;
		next;
		
	#確認画面
	} elsif ($k =~ /^_CONFIRMATION(?:PAGE|)$/) {
		next;
		
	#データを添付
	} elsif ($k =~ /^_DATA$/) {
		$v = $1 if $v =~ /^(.*?)\0/;
		$sv = $v;
		next;
		
	#番号の自動発行
	} elsif ($k =~ /^_ID(-[0-9a-zA-Z]+|)(_.*|)$/) {
		($id_ext = $1) =~ s/^-//;
		$id_name = '登録番号' if ($id_name = $3) =~ s/^_//;
		$v = $1 if $v =~ /^(.*?)\0/;
		$id_file = $v;
		next;
		
	#自動返信メール
	} elsif ($k =~ /^_MSG(_.*|)$/) {
		($msg_title = $1) =~ s/^_//;
		$v = $1 if $v =~ /^(.*?)\0/;
		$msg_file = $v;
		next;
		
	#名前
	} elsif ($k =~ /^_NAME(_.*|)$/) {
		($k = $1) =~ s/^_//;
		$k = 'お名前' if !$k;
		$user_name .= (($user_name) ? ' ' : '') . join(' ',grep($_ ne '',split(/\0/,$v)));

	#ヘッダの処理
	} elsif ($k =~ /^_([^_]+)/i) {
		$header = $1;
		$header =~ s/(\w+)/ucfirst(lc $1)/eg;
		my $header_v = $v;
		$header_v =~ s/\0/,/g;

		next if $header =~ /^($to)$/i && $send_ok == 0;
		$format = 'E' if (!$format || $format !~ /e/i) && $header =~ /^($to|$from)$/i;
		if ($header_v ne '') {
			if (grep($_ eq $header,'To','Cc','Bcc','From','Reply-To')) {
				my @emails = $input->get_address((($mail_header{$header}) ? $mail_header{$header} : ()),$header_v);
				$mail_header{$header} = join(', ',@emails);
			} else {
				$mail_header{$header} .= ((defined $mail_header{$header} && $mail_header{$header} ne '') ? ', ' : '') . $header_v;
			}
		}
		if ($k =~ /^_$header\_(.*)$/i) {
			$k = $1;
			if (!defined $k || $k eq '') {
				if ($header eq 'To' || $header eq 'Cc') {
					$k = '宛先アドレス';
					$skip = 1;
				} elsif ($header eq 'From') {
					$k = '差出人アドレス';
				} elsif ($header eq 'Reply-To') {
					$k = '返信先アドレス';
				} elsif ($header eq 'Subject') {
					$k = 'タイトル';
				} else {
					$skip = 1 if $header eq 'Bcc';
					$k = $header;
				}
			}
		} else {
			$skip = 1;
			$k = $header;
		}
		if ($header eq 'Subject') {
			my $name = $user_name || 'お客';
			$v =~ s/_ID_/$number/gi;
			$v =~ s/_NAME_/$name/gi;
		}
	}

	#入力チェックスキップ
	next if $no_check;

	#入力チェック
	if ($required && $v eq '') {
		push(@error,$k . 'が入力されていません。');
		$is_invalid = 1;
	}

	#形式チェック
	if (($format ne '' && $v ne '') || $check) {
		my(@values,$invalid);
		$invalid = 0;
		@values = split(/\0/,$v,-1);
		if ($format eq 'E' && grep($_ ne '' && $input->is_invalid_email_address_header($_),@values)) {
			push(@error,$k . 'がメールアドレスではありません。');
			$is_invalid = 1;
		} elsif ($format eq 'e' && grep($_ ne '' && $input->is_invalid_email_address($_),@values)) {
			push(@error,$k . 'がメールアドレスではありません。');
			$is_invalid = 1;
		} elsif ($format eq 'N' || $format eq 'n') {
			my $nocal = ($format eq 'N') ? 1 : 0;
			map($invalid = ($_ ne '' && $input->is_nan($_,$nocal)) ? 1 : $invalid,@values);
			$input{$key} = join("\0",@values) if $input{$key};
			if ($invalid) {
				push(@error,$k . 'を半角数字にしてください。');
				$is_invalid = 1;
			}
		} elsif ($format eq 'a') {
			map($invalid = ($_ ne '' && $input->is_not_word($_)) ? 1 : $invalid,@values);
			$input{$key} = join("\0",@values) if $input{$key};
			if ($invalid) {
				push(@error,$k . 'を半角英数字にしてください。');
				$is_invalid = 1;
			}
		} elsif ($format eq 'A') {
			map($invalid = ($_ ne '' && $input->is_not_word($_,1)) ? 1 : $invalid,@values);
			$input{$key} = join("\0",@values) if $input{$key};
			if ($invalid) {
				push(@error,$k . 'を半角英数字にしてください。');
				$is_invalid = 1;
			}
		} elsif ($format eq 'K') {
			map($invalid = ($_ ne '' && $input->is_not_katakana($_)) ? 1 : $invalid,@values);
			$input{$key} = join("\0",@values) if $input{$key};
			if ($invalid) {
				push(@error,$k . 'をカタカナにしてください。');
				$is_invalid = 1;
			}
		} elsif ($format eq 'H') {
			map($invalid = ($_ ne '' && $input->is_not_hiragana($_)) ? 1 : $invalid,@values);
			$input{$key} = join("\0",@values) if $input{$key};
			if ($invalid) {
				push(@error,$k . 'をひらがなにしてください。');
				$is_invalid = 1;
			}
		} elsif ($format eq 'U' && grep($_ ne '' && $input->is_invalid_url($_),@values)) {
			push(@error,$k . 'がURLではありません。');
			$is_invalid = 1;
		} elsif ($format eq 'p' && grep($_ ne '' && $input->is_invalid_password($_,$offset,$limit),@values)) {
			push(@error,$k . 'は' . (($offset) ? $offset . '文字以上' : '') . (($limit) ? $limit . '文字以下の\n' : (($offset) ? 'の\n' : '')) . '半角英数字列にしてください。');
			$is_invalid = 1;
		} elsif ($format eq 'P' && grep($_ ne '' && $input->is_invalid_password($_,$offset,$limit,1),@values)) {
			push(@error,$k . 'は半角英字から始まる\n' . (($offset) ? $offset . '文字以上' : '') . (($limit) ? $limit . '文字以下の\n' : (($offset) ? 'の\n' : '')) . '半角英数字列にしてください。');
			$is_invalid = 1;
		}

		#重複チェック
		if ($check && grep($_ ne '',@values)) {
			my($temp);
			foreach my $value (@values) {
				if (defined $temp) {
					if ($temp ne $value) {
						push(@error,$k . 'が一致しません。');
						$is_invalid = 1;
					}
				} else {
					if ($value eq '') {
						push(@error,$k . 'が入力されていません。');
						$is_invalid = 1;
					}
					$temp = $value;
				}
			}
			if (!$is_invalid && !$skip) {
				$in{$key} = $v = $temp;
				if ($format eq 'P' || $format eq 'p') {
					$passwd = $temp;
					$passwords{$k}++;
				}
			}
		}
	}
	if ($skip) {
		next;
	} elsif ($is_invalid) {
		push(@invalid_fields,$key) if !@invalid_fields || !grep($_ eq $key,@invalid_fields);
		next;
	}
	if (@files) {
		$input->save_file(
			$key,
			'!' . $input->parameter_directory_name($key),
		);
	}
	$v = join(', ',grep($_ ne '',split(/\0/,$v)));

	if ($action eq 'P') {
		next;
	
	} elsif ($action eq 'C') {
		push(@header,$k);
		push(@data,$v);
	
	} else {
		$v =~ s/\x0D\x0A/\x0A/sg;
		$v =~ s/\x0D/\x0A/sg;

		push(@header,$k);
		push(@data,$v);
	
		if ($v ne '') {
			$message .= '[' . $k . "]\x0A" . $v . "\x0A\x0A";
		}
	}
}
undef %count;

#記入漏れがあれば書き込みページに戻る
$this->print_form_page($input,$referer,\%input,\@error,\@invalid_fields) if !$no_check && @error;

#前後ページへジャンプ
if ($action eq 'P') {
	my(@err);
	if (!defined $nextpage || $nextpage eq '') {
		$nextpage = $referer;
		push(@err,'移動先が設定されていません。');
	}
	$this->print_form_page($input,$nextpage,\%input,\@err);

#入力確認画面
} elsif ($action eq 'C') {
	$this->print_confirmation_page($input,$nextpage,$referer,\%input,\@header,\@data,\%passwords);
}

#会員番号
if ($id_file && $id_file !~ m!/!) {
	$number = $this->number_update($input,$number_dir . '/' . $id_file) . $id_ext;
	if ($number) {
		$message = $id_name . ' : ' . $number . "\x0A\x0A" . $message;
		if (defined $sv && $sv) {
			unshift(@header,$id_name);
			unshift(@data,$number);
		}
	}
}

#添付データ整形
if (defined $sv && $sv) {
	my($s,$type,@header2,@data2);
	if ($sv =~ /tsv/i) {
		$data{'name'} = 'data.tsv';
		$data{'type'} = 'text/tab-separated-values';
		$s = "\x09";
		$type = 'タブ区切りテキスト';
	} else {
		$data{'name'} = 'data.csv';
		$data{'type'} = 'text/comma-separated-values';	
		$s = ',';
		$type = 'CSV形式ファイル';
	}

	@header2 = @header;
	@data2 = @data;
	map($input->jcode_convert(\$_,'sjis','utf8'), @header2);
	map($input->jcode_convert(\$_,'sjis','utf8'), @data2);
	$data{'data'} = $input->svjoin($s,@header2) . "\x0D\x0A";
	$data{'data'} .= $input->svjoin($s,@data2);
	undef @header2;
	undef @data2;

	push(@files,\%data);
	if ($sv =~ /_$/) {
		$mail_header{'message'} = '下記内容を受信しました。' . "\x0A" . '------------------------------------------------------------' . "\x0A\x0A" . $message;
	}
	$mail_header{'message'} .= '※送信されたデータが' . $type . 'で添付されています。';
} else {
	$mail_header{'message'} = '下記内容を受信しました。' . "\x0A" . '------------------------------------------------------------' . "\x0A\x0A" . $message;
}

#送信タイトル
$user_name = 'お客' if !$user_name;
if ($mail_header{'Subject'}) {
	$mail_header{'Subject'} =~ s/_ID_/$number/gi;
	$mail_header{'Subject'} =~ s/_NAME_/$user_name/gi;
}

require CMONOS::CGI_Lib::SendMail;
$mail = SendMail->new($sendmail,$cgi_master,$sizelimit);

#メール送信
if (@files) {
	$mail_header{'file'} = \@files;
	$mail_header{'input'} = $input;
}

#送信できなかった場合
if (!$mail->send_mail(%mail_header)) {
	my(@error_msg);
	push(@error_msg,$input->dialog,$mail->dialog);
	$this->print_form_page($input,$referer,\%input,\@error_msg);
}

#クリップボードクリア
$input->clear_parameters_trash;
$input->clear_clipboard;

#自動返信
if ($msg_file) {
	if ($msg_file =~ /==/) {
		my $msg_file_name2 = '';
		my $msg_file_name = '';
		my @conditions = split(/\|\|/,$msg_file);
		foreach my $cond (@conditions) {
			$cond =~ s/[\x20\x09\x0a\x0d]//sg;
			if ($cond =~ /^(.*?)==(.*?)==(.*)$/) {
				my($k,$v,$path) = ($1,$2,$3);
				if (defined $in{$k}) {
					my @val = split(/\0/,$in{$k},-1);
					if (grep($v eq $_,@val)) {
						$msg_file_name = $path;
						last;
					}
				}
			} else {
				$msg_file_name2 = $cond;
			}
		}
		$msg_file = $msg_file_name || $msg_file_name2;
	}
	if ($msg_file && $msg_file !~ m!/!) {
		$msg = $input->read_file($msg_dir . '/' . $msg_file);
		if ($msg =~ s/^Subject:\s*(.*?)[\x0a\x0D]+//s) {
			$msg_title = $1;
		} elsif ($msg eq '') {
			$msg = 'ありがとうございます。' . "\x0A" . '下記内容が送信されました。' . "\x0A\x0A" . '------------------------------------------------------------' . "\x0A\x0A" . '<data>';
		}
		$msg_title = 'ご記入ありがとうございます。' if !defined $msg_title || !$msg_title;
		$msg =~ s/<id>/$number/gi;
		$msg =~ s/<password>/$passwd/gi;
		$msg =~ s/<master_email>/$cgi_master/gi;
		$msg =~ s/<email>/$mail_header{'To'}/gi;
		$msg =~ s/<data>/$message/gi;
		$msg =~ s/<name>/$user_name/gi;
		$mail->send_mail(
			'From' => $mail_header{'To'},
			'To' => (($mail_header{'From'}) ? $mail_header{'From'} : $mail_header{'Reply-To'}),
			'Subject' => $msg_title,
			'message' => $msg,
			'info' => 0
		);
	}
}
undef $message;

#thankspageが相対パスで指定されている場合
if ($thanks_page) {
	if ($thanks_page =~ /==/) {
		my $thanks_page_path2 = '';
		my $thanks_page_path = '';
		my @conditions = split(/\|\|/,$thanks_page);
		foreach my $cond (@conditions) {
			$cond =~ s/[\x20\x09\x0a\x0d]//sg;
			if ($cond =~ /^(.*?)==(.*?)==(.*)$/) {
				my($k,$v,$path) = ($1,$2,$3);
				if (defined $in{$k}) {
					my @val = split(/\0/,$in{$k},-1);
					if (grep($v eq $_,@val)) {
						$thanks_page_path = $path;
						last;
					}
				}
			} else {
				$thanks_page_path2 = $cond;
			}
		}
		$thanks_page = $thanks_page_path || $thanks_page_path2;
	}
	if ($thanks_page) {
		$thanks_page_jump = ($thanks_page =~ s/^\!+//) ? 1 : 0;
		if ($thanks_page !~ /^\// && $input->is_invalid_url($thanks_page)) {
			$thanks_page = $input->path_change($thanks_page,$referer,'abs');
		}
	}
}

#入力のお礼
$input->jump($input->full_path($thanks_page)) if $thanks_page_jump;
my $form = $this->get_referer_html($input,(($thanks_page) ? $thanks_page : $referer));
$input->jump($thanks_page) if !$form && $thanks_page && $thanks_page =~ /^https?:\/\//i;

my $data_table = '<table class="field-table"><tbody>' . $this->data_table($input,\@header,\@data,\%passwords) . '</tbody></table>';
$msg_title = 'ご記入ありがとうございます。' if !defined $msg_title || !$msg_title;
$msg = '<p>ありがとうございます。下記内容が送信されました。</p>' . $data_table;

if (!$form) {
	$form = '<html><head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8" /><title>' . $msg_title . '</title></head><body>' . $msg . '</body></html>';
} else {
	$form =~ s/<!--FORM_ONLY-->.*?<!--\/FORM_ONLY-->//sg;
	$form =~ s/<!--THANKS:(.*?)-->/$1/sg;
	$form =~ s/(<\/title>)/:$msg_title$1/si if $form =~ s/(<form\s+[^>]*action\s*=\s*"?[^"]*postman\.cgi"?[^>]*>.*?<\/form>)/$msg/ies;
	$form =~ s/<id>/$number/gi;
	$form =~ s/<password>/$passwd/gi;
	$form =~ s/<master_email>/$cgi_master/gi;
	$form =~ s/<email>/$mail_header{'To'}/gi;
	$form =~ s/<data>/$data_table/gi;
	$form =~ s/<name>/$user_name/gi;
}

#書き出し
print 'Cache-Control: no-cache',"\x0A";
print 'Pragma: no-cache',"\x0A";
print 'Content-Type: text/html',"\x0A";
print "\x0A";
print $form;
exit;

########################################################################
#確認ページ
sub print_confirmation_page ($$$$$$$$) {
my($this,$input,$confirmationpage,$referer,$in,$header,$data,$passwords) = @_;
my($form,$start,$end,$thanks,$has_tags,$use_form);

$form = $this->get_referer_html($input,($confirmationpage) ? $confirmationpage : $referer);
$has_tags = 1 if $form =~ s/<!--FORM_ONLY-->.*?<!--\/FORM_ONLY-->//sg;
$has_tags = 1 if $form =~ s/<!--CONFIRMATION:(.*?)-->/$1/sg;
$use_form = 1 if $form !~ /<input[^>]*\sname="(?:\d+_|)_(?:PREV|NEXT)[^"]*"[^>]*>/si;

#呼び出し元を元に作成
if ($form =~ /\A(.*?<form\s+[^>]*action\s*=\s*"?[^"]*postman\.cgi"?[^>]*>)(.*?)(<\/form>.*)\Z/is) {
	$start = $1;
	$form = $2;
	$end = $3;
	undef $form if !$use_form;
	$start =~ s/(<\/title>)/ : 送信内容の確認$1/si if !$has_tags;

#呼び出し元が取得できない場合
} else {
	$start = '<html><title>送信内容の確認</title><meta http-equiv="Content-Type" content="text/html;charset=UTF-8" /><body><form action="./postman.cgi" method="POST">';
	$end = '</form></body></html>';
	undef $form;
}

#ヘッダ
print 'Cache-Control: no-cache',"\x0A";
print 'Pragma: no-cache',"\x0A";
print 'Content-Type: text/html',"\x0A";
print "\x0A";
print $start;
print '<input type="hidden" name="_" value="＿" />';
print '<input type="hidden" name="_CLIPBOARD" value="' . $input->escape($input->{'clipboard_id'}) . '" />' if ref $input && $input->{'clipboard_id'} && !$input->{'clipboard_expired'};

#値のトス
while (my($k,$v) = each %$in) {
	next if $k =~ /(^|&)(\d+_|)_(REFERER|HERE|CONFIRMATION|NEXT|PREV|CONFIRMATIONPAGE|NEXTPAGE|PREVPAGE|CANCEL|NOCHECK|DELETE|CLIPBOARD)(=|$)/;
	$thanks++ if $k =~ /(^|&)(\d+_|)_THANKS(=|$)/;
	my @ky = split(/\0/,$v,-1);
	push(@ky,'') if !@ky;
	foreach my $value (@ky) {
		print '<input type="hidden" name="' . $input->escape($k) . '" value="' . $input->escape($value) . '" />';
	}
}
print '<input type="hidden" name="_REFERER" value="' . $referer . '" />';
print '<input type="hidden" name="_THANKS" value="' . $confirmationpage . '" />' if $confirmationpage && !$thanks;

#一覧表
if ($form) {
	print $this->replace_fields($form,$input,$in);
} else {
	print '<div id="form-confirmation"><strong>下記内容に問題がなければ「送信」ボタンを押してください。</strong></div><table class="field-table"><tbody>';
	print $this->data_table($input,$header,$data,$passwords);
	print '</td></tr></tbody><tbody>';
	print '<tr><td colspan="2" class="submit-box"><input type="submit" name="_CANCEL" value="キャンセル" class="cancel" /> <input type="submit" value="送信する" class="save" /></td></tr>';
	print '</tbody></table>';
}

#フッタ
print $end;
exit;
}

sub replace_fields ($$$$) {
my($this,$form,$input,$in) = @_;
my($cancel_button_is_found,$submit_button_is_found);
while (my($k,$v) = each %$in) {
	next if $k =~ /(^|&)(\d+_|)_(REFERER|HERE|CONFIRMATION|NEXT|PREV|CONFIRMATIONPAGE|NEXTPAGE|PREVPAGE|CANCEL|DELETE|CLIPBOARD|MSG|THANKS|DATA)(_|=|$)/;
	my @values = (defined $v) ? grep($_ ne '*',split(/\0/,$v,-1)) : ();
	my $key = $k;
	$k = quotemeta $k;
	if ($form =~ s/<!--FIELD:$k-->.*?<!--\/FIELD-->/$this->field_value($input,\@values)/gse) {
		next;
	} else {
		$form =~ s/\s*<label[^>]*>\s*<(input|button)([^>]*\s+name="$k"[^>]*)>(.*?)\s*<\/label>[\x09\x20]*/$this->shift_field_value($input,$key,\@values,$2,$3)/gise;
		$form =~ s/\s*<label[^>]*>\s*<textarea[^>]*\s+name="$k"[^>]*>(.*?)<\/textarea>(.*?)<\/label>[\x09\x20]*/$this->shift_field_value($input,$key,\@values,'',$2,$input->unescape($1))/gise;
		$form =~ s/\s*<label[^>]*>\s*<select[^>]*\s+name="$k"[^>]*>.*?<\/select>(.*?)<\/label>[\x09\x20]*/$this->field_value($input,\@values). $1/gise;
		$form =~ s/<(input|button)([^>]*\s+name="$k"[^>]*)>([^<>]*)\s*/$this->shift_field_value($input,$key,\@values,$2,$3)/gise;
		$form =~ s/<textarea[^>]*\s+name="$k"[^>]*>(.*?)<\/textarea>([^<>]*)\s*/$this->shift_field_value($input,$key,\@values,'',$2,$input->unescape($1))/gise;
		$form =~ s/<select[^>]*\s+name="$k"[^>]*>.*?<\/select>([^<>]*)\s*/$this->field_value($input,\@values). $1/gise;
	}
	$form =~ s/\s*<label[^>]*>\s*<(input|button|textarea|select)[^>]*\s+name="$k"[^>]*>(?:.*?<\/\1>|).*?\s*<\/label>[\x09\x20]*//sig;
	$form =~ s/<(input|button|textarea|select)[^>]*\s+name="$k"[^>]*>(?:.*?<\/\1>|)//sig;
}
$form =~ s/\s*<label[^>]*>\s*<(input|button|textarea|select)([^>]*)>(?:.*?<\/\1>|).*?\s*<\/label>[\x09\x20]*/$this->append_submit_button($2,\$cancel_button_is_found,\$submit_button_is_found)/sieg;
$form =~ s/<(input|button|textarea|select)([^>]*)>(?:.*?<\/\1>|)/$this->append_submit_button($2,\$cancel_button_is_found,\$submit_button_is_found)/sieg;
$form =~ s/\s*<li[^>]*>\s*<\/li>[\x09\x20]*//sig;
$form =~ s/\s*<ol[^>]*>\s*<\/ol>[\x09\x20]*//sig;
$form =~ s/\s*<ul[^>]*>\s*<\/ul>[\x09\x20]*//sig;
$form =~ s/<\/?label[^>]*>//sig;
if (!$submit_button_is_found) {
	$form .= '<input type="submit" value="送信する" class="save" />';
}
if (!$cancel_button_is_found) {
	$form =~ s/(<input[^>]*\stype=["']?submit["']?[^>]*>)/<input type="submit" name="_CANCEL" value="キャンセル" class="cancel" \/> $1/si;
}
return $form;
}

sub shift_field_value ($$$$$;$$) {
my($this,$input,$k,$v,$attributes,$label,$value) = @_;
my $type = (defined $value) ? 'textarea' : ($attributes =~ /\stype=["'](.*?)["']/) ? lc $1 : '';
$value = ($attributes =~ /\svalue=["'](.*?)["']/) ? $input->unescape($1) : '' if !defined $value && $attributes;
if ($type eq 'checkbox' || $type eq 'radio') {
	if (defined $value) {
		my $field_value;
		my @temp;
		foreach my $val (@$v) {
			if (!defined $field_value && $val eq $value) {
				$field_value = $input->escape($value);
			} else {
				push(@temp,$val);
			}
		}
		@$v = @temp;
		return $field_value || '';
	}
} elsif ($type eq 'file') {
	@$v = ();
	return $this->get_attachment_sample($input,$k);
} elsif ($type eq 'password') {
	my $val = shift(@$v);
	return ('*' x length($val)) . ($label || '');
} elsif ($type eq 'hidden') {
	return '';
} else {
	my $val = $input->escape(shift(@$v));
	return ($val ne '') ? $val . ($label || '') : '';
}
}

sub field_value ($$$) {
my($this,$input,$v) = @_;
if (@$v > 1) {
	my $value = '<ol class="field-value">';
	foreach my $data (@$v) {
		$value .= '<li>' . $input->lf_to_tag($input->escape($data)) . '</li>';
	}
	$value .= '</ol>';
	@$v = ();
	return $value;
} else {
	return shift(@$v) || '';
}
}

sub append_submit_button ($$$$) {
my($this,$attributes,$cancel_button_is_found,$submit_button_is_found) = @_;
my $name = ($attributes =~ /\sname="(.*?)"/si || $attributes =~ /\sname='(.*?)'/si) ? $1 : '';
my $type = ($attributes =~ /\stype="(.*?)"/si || $attributes =~ /\stype='(.*?)'/si) ? lc $1 : '';
if ($type eq 'submit') {
	if ($name =~ /_CANCEL/) {
		$$cancel_button_is_found++;
		return '<input' . $attributes . '>';
	} elsif ($name eq '') {
		my $value = ($attributes =~ /\svalue="(.*?)"/si || $attributes =~ /\svalue='(.*?)'/si) ? $1 : '';
		$$submit_button_is_found++;
		if ($value =~ /確認/) {
			$attributes =~ s/\svalue=["']$value["']/ value="送信する"/si
		} elsif ($value =~ /confirm/i) {
			$attributes =~ s/\svalue=["']$value["']/ value="Submit"/si
		}
		return '<input' . $attributes . '>';
	}
}
return '';
}

sub data_table ($$$$$) {
my($this,$input,$header,$data,$passwords) = @_;
my($table);
foreach my $n (0..$#{$header}) {
	my $h = $$header[$n];
	my $d = $$data[$n];
	if ($$passwords{$h}) {
		$d = '*' x length($d)
	} else {
		$d = $input->escape($d);
		$d =~ s/(\x0D\x0A|\x0D|\x0A)/<br \/>/gs;
	}
	$h = $input->escape($h);
	$h =~ s/(\x0D\x0A|\x0D|\x0A)/<br \/>/gs;
	$table .= '<tr><td class="field-name"><span class="datatitle">' . $h . '</span></td><td class="field">' . $d . '</td></tr>';
}
return $table;
}

sub get_attachment_sample ($$$$;$) {
my($this,$input,$h,$files,$is_form) = @_;
@$files = $input->get_posted_file_numbers($h) if !ref $files || !defined @$files;
my $d = '';
if (ref $files && @$files) {
	require CMONOS::CGI_Lib::Image;
	my $image = Image->new;
	my @file_names;
	foreach my $num (@$files) {
		my %properties = $input->get_posted_file_properties_from_param($h,(($num) ? $num : 0));
		if ($properties{'savedir'} && $properties{'savename'} && -f $properties{'savedir'} . '/' . $properties{'savename'}) {
			my $path = $properties{'savedir'} . '/' . $properties{'savename'};
			my $name = $properties{'filename'} || 'FILE';
			$name = $input->escape($name);
			$name =~ s/(\x0D\x0A|\x0D|\x0A)/<br \/>/gs;
			if ($path) {
				if ($path =~ /\.(?:jpg|jpeg|png|gif)$/i) {
					$d .= '<div class="attachments">' . $image->tag(
						$path,
						0,
						$name,
						'',
						300,
						300,
					) . '</div>';
				} else {
					$d .= '<div class="attachments"><a href="' . $path . '" target="_blank">' . $name . '</a></div>';
				}
			}
			push(@file_names,$properties{'filename'});
		}
	}
	if (@file_names) {
		foreach my $n (@file_names) {
			$d .= '<input type="hidden" name="' . $input->escape($h) . '" value="' . $input->escape($n) . '" />';
		}
	} else {
		$d .= '<input type="hidden" name="' . $input->escape($h) . '" value="*" />';
	}
	if ($is_form) {
		$d .= '<div class="attachments-reset"><label><input type="checkbox" name="_DELETE" value="' . $input->escape($h) . '" /> ' . ((@$files > 1) ? 'これら' : 'こ') . 'のファイルを削除する</label></div>';
	}
}
return $d;
}

########################################################################
#フォーム読み込み→表示
sub print_form_page ($$$$$$;$) {
my($this,$input,$referer,$in,$msg,$invalid_fields) = @_;
my($form);

$form = $this->get_referer_html($input,$referer,$msg);

#デフォルトの作成
if ($form && $form =~ s/(<form\s+[^>]*action\s*=\s*"?[^"]*postman\.cgi"?[^>]*>)(.*?)(<\/form>)/$1 . $this->mk_default_value($2,$in,$input,$invalid_fields) . '<input type="hidden" name="_REFERER" value="' . $referer . '" \/>' . $3/iges) {
	print 'Cache-Control: no-cache',"\x0A";
	print 'Pragma: no-cache',"\x0A";
	print 'Content-Type: text/html',"\x0A";
	print "\x0A";
	print $form;

#呼び出し元が取得できない場合
} else {
	my $alert = '';
	foreach my $m (@$msg) {
		next if !defined $m || $m eq '';
		$m =~ s/'//g;
		$alert .= "alert('$m');";
	}
	$input->print_http_header;
	print '<html><head>';
	print '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" /><title>入力に問題があります。</title></head>';
	print '<body onload="history.back();' . $alert . '"' . '>ブラウザの「戻る」ボタンで前のページに戻ってください。</body></html>';
#	$input->jump($referer);
}
exit;
}

#デフォルトの作成
sub mk_default_value ($$$$;$) {
my($this,$form,$in,$input,$invalid_fields) = @_;
return $form unless ref $in && %$in;
my @keys = keys %$in;

# input
$form =~ s/(<input[^>]*\s+name\s*=\s*"?([^"\s]+)"?[^>]*>)/$this->mk_default_input($2,$1,$in,$input,\@keys,$invalid_fields)/iges;

# select
$form =~ s/(<select\s+[^>]*name\s*=\s*"?([^"\s]+)"?[^>]*>)(.*?)(<\/select>)/$1 . $this->mk_default_menu($2,$3,$in,$input,\@keys,$invalid_fields) . $4/iges;

# textarea
$form =~ s/(<textarea\s+[^>]*name\s*=\s*"?([^"\s]+)"?[^>]*>)(.*?)(<\/textarea>)/$1 . $this->mk_default_text($2,$3,$in,$input,\@keys,$invalid_fields) . $4/iges;

while (my($k,$v) = each %$in) {
	next if $k =~ /(^|&)(\d+_|)_(REFERER|HERE|CONFIRMATION|NEXT|PREV|CONFIRMATIONPAGE|NEXTPAGE|PREVPAGE|CANCEL|DELETE|CLIPBOARD)(=|$)/ || !grep($_ eq $k,@keys);
	my(@values,$dammy);
	@values = split(/\0/,$v,-1);
	push(@values,'') if !@values;
	VAL:
	foreach my $val (@values) {
		if ($val eq '*') {
			next VAL if $dammy;
			$dammy++;
		}
		$form .= '<input type="hidden" name="' . $input->escape($k) . '" value="' . $input->escape($val) . '" />';
	}
}

$form = '<input type="hidden" name="_CLIPBOARD" value="' . $input->escape($input->{'clipboard_id'}) . '" />' . $form if ref $input && $input->{'clipboard_id'} && !$input->{'clipboard_expired'};

return $form;
}

sub mk_default_input ($$$$$$;$) {
my($this,$name,$form,$in,$input,$keys,$invalid_fields) = @_;
$name = $input->unescape($name);

#特殊変数
return $form if $name =~ /(^|&)(\d+_|)_(REFERER|HERE|CONFIRMATION|NEXT|PREV|CONFIRMATIONPAGE|NEXTPAGE|PREVPAGE|CANCEL|DELETE|CLIPBOARD)(=|$)/;

@$keys = grep($_ ne $name,@$keys);

my $type = ($form =~ /\s+type\s*=\s*"?([^"]+)"?/si) ? lc $1 : 'text';
$form = $this->append_invalid_fields_class($name,$form,$invalid_fields);

my @values = (defined $in->{$name}) ? split(/\0/,$in->{$name},-1) : ();
if (grep($_ eq $type,'text','search','tel','url','email','password','datetime','date','month','week','time','datetime-local','number','range','color')) {
	my $value = $input->escape(shift(@values));
	$form =~ s/\s*\/?>$/ value="$value" \/>/ unless $form =~ s/\s+value\s*=\s*"?[^"]*"?/ value="$value"/sig;

} elsif ($type eq 'file') {
	$form .= $this->get_attachment_sample($input,$name,undef,1);

} elsif ($type eq 'hidden' || $type eq 'submit') {
	my $value = ($form =~ /\s+value\s*=\s*"?([^"]+)"?/si) ? $input->unescape($1) : '';
	@values = grep($_ ne $value,@values);

} elsif ($type eq 'checkbox' || $type eq 'radio') {
	my $value = ($form =~ /\s+value\s*=\s*"?([^"]+)"?/si) ? $input->unescape($1) : '';
	if (grep($_ eq $value,@values)) {
		$form =~ s/\s*\/?>$/ checked="checked" \/>/ unless $form =~ /\s+checked(\s*=\s*"?checked"?|)/si;
		@values = grep($_ ne $value,@values);
	} else {
		$form =~ s/\s+checked(\s*=\s*"?checked"?|)//sig
	}
}

$form =~ s/([^\/])>$/$1 \/>/;
$in->{$name} = join("\0",@values) if @values;
return $form;
}

sub append_invalid_fields_class ($$$$) {
my($this,$name,$form,$invalid_fields) = @_;
if (ref $invalid_fields && grep($_ eq $name,@$invalid_fields)) {
	my $class = ($form =~ /\s+class\s*=\s*["']?([^"']+)["']?/si) ? $1 : '';
	if ($class !~ /invalid-field/) {
		$class .= (($class) ? ' ' : '') . 'invalid-field';
		$form =~ s/\s*\/?>$/ class="$class" \/>/ unless $form =~ s/\s+class\s*=\s*["']?([^"']+)["']?/ class="$class"/si;
	}
}
return $form;
}

sub mk_default_menu ($$$$$$;$) {
my($this,$name,$menu,$in,$input,$keys,$invalid_fields) = @_;
my(@input);
$name = $input->unescape($name);
return $menu unless defined $$in{$name};
$menu = $this->append_invalid_fields_class($name,$menu,$invalid_fields);
@$keys = grep($_ ne $name,@$keys);
$menu =~ s/\s*<option([^>]*)>([^<]*)(<\/option>|)/$this->mk_default_option($1,$2,$in,$name,$input)/sige;
return $menu;
}

sub mk_default_option ($$$$$$) {
my($this,$option,$v,$in,$name,$input) = @_;
my $value = $input->unescape(($option =~ s/\s+value\s*=\s*"?([^"]*)"?//sig) ? $1 : $v);
my @values = (defined $in->{$name}) ? split(/\0/,$in->{$name},-1) : ();
if (grep($_ eq $value,@values)) {
	$option .= ' selected="selected"' unless $option =~ /\s+selected(\s*=\s*"?selected"?|)/sig;
	@values = grep($_ ne $value,@values);
} else {
	$option =~ s/\s+selected(\s*=\s*"?selected"?|)//sig;
}
return '<option value="' . $input->escape($value) . '"' . $option . '>' . $input->escape($v) . '</option>';
}

sub mk_default_text ($$$$$$;$) {
my($this,$name,$text,$in,$input,$keys,$invalid_fields) = @_;
$name = $input->unescape($name);
return $text unless defined $$in{$name};
$text = $this->append_invalid_fields_class($name,$text,$invalid_fields);
@$keys = grep($_ ne $name,@$keys);
my @values = split(/\0/,$$in{$name},-1);
$text = $input->escape(shift(@values));
$$in{$name} = join("\0",@values);
return $text;
}

########################################################################
#呼び出し元ＨＴＭＬ読み込み
sub get_referer_html ($$$;$) {
my($this,$input,$referer,$alert) = @_;
my($form,$referer_path);
return '' if !defined $referer || $referer eq '' || $referer !~ /\.(html|htm)$/i || $referer =~ m!\./!;
($referer_path = $referer) =~ s/^https?:\/\/[^\/]+//i;
$referer_path = $input->path_change($referer_path,$ENV{'SCRIPT_NAME'},'rel');
$form = $input->read_file($referer_path);
return '' if !defined $form || $form eq '';

$form =~ s/(?:\x0D\x0A|\x0D)/\x0A/sg;
$form =~ s/(<[^<>]*[\x09\x0A\x0C\x0D\x20]+(?:href|src|background|action)=["']?)(?![0-9a-zA-Z_]+:)([^"\x09\x0A\x0C\x0D\x20]+)([^<>]*>)/$1 . $input->un_base_change($2,$referer_path,'inherit') . $3/seig;
$form =~ s/(<param[\x09\x0A\x0C\x0D\x20]+name=["']?(?:src|movie)["']?[\x09\x0A\x0C\x0D\x20]+value=["']?)(?![0-9a-zA-Z_]+:)([^"\x09\x0A\x0C\x0D\x20]+)([^<>]*>)/$1 . $input->un_base_change($2,$referer_path,'inherit') . $3/seig;
$form =~ s/(<video(?![0-9a-zA-Z_])[^<>]*[\x09\x0A\x0C\x0D\x20]+preview=["']?)(?![0-9a-zA-Z_]+:)([^"\x09\x0A\x0C\x0D\x20]+)([^<>]*>)/$1 . $input->un_base_change($2,$referer_path,'inherit') . $3/seig;

unless ($form =~ s/<meta\s+[^>]*http-equiv\s*=\s*"?Content-Type"?[^>]*>/<meta http-equiv="Content-Type" content="text\/html; charset=UTF-8" \/>/is) {
	$form =~ s/(<\/head>)/<meta http-equiv="Content-Type" content="text\/html; charset=UTF-8" \/>$1/is;
}
unless ($form =~ s/<meta\s+[^>]*http-equiv\s*=\s*"?Content-Script-Type"?[^>]*>/<meta http-equiv="Content-Script-Type" content="text\/javascript" \/>/is) {
	$form =~ s/(<\/head>)/<meta http-equiv="Content-Script-Type" content="text\/javascript" \/>$1/is;
}
unless ($form =~ s/<meta\s+[^>]*http-equiv\s*=\s*"?Content-Style-Type"?[^>]*>/<meta http-equiv="Content-Style-Type" content="text\/css" \/>/is) {
	$form =~ s/(<\/head>)/<meta http-equiv="Content-Style-Type" content="text\/css" \/>$1/is;
}

if (ref $alert && @$alert) {
	my $msg;
	foreach (@$alert) {
		$msg .= 'alert(\'' . $_ . '\'); ';
	}
	unless ($form =~ s/(<body\s+[^>]*onload\s*=\s*"?)([^"]*"?[^>]*>)/$1$msg$2/is) {
		$form =~ s/(<body[^>]*)(>)/$1 onload="$msg"$2/is;
	}
}
return $form;
}

########################################################################
#登録番号更新
sub number_update ($$$) {
my($this,$input,$path) = @_;
my $num = $input->read_file($path);
my $d = length $num;
$d = 4 if !$d;
$num = sprintf("%.${d}d",$num+1);
$input->write_file($path,$num);
return $num;
}

