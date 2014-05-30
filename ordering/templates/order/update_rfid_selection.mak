% if rfid == "YES":
% if rfid_order_flag == "YES":
<div class="rfid_brand">
Please select the ticket stock number:
&nbsp;&nbsp;
% if brand_type == "N":
<select name="national_brand">
	<option value=""></option>
	<option value=""></option>
	<option value="0214">0214</option>
	<option value="0215">0215</option>
	<option value="0802">0802</option>
	<option value="0803">0803</option>
	<option value="0805">0805</option>
	<option value="0809">0809</option>
	<option value="0810">0810</option>
	<option value="0811">0811</option>
	<option value="0813">0813</option>
	<option value="0814">0814</option>
    <option value="0824">0824</option>
	<option value="0826">0826</option>
	<option value="0988">0988</option>
	<option value="9822">9822</option>
	<option value="9823">9823</option>
	<option value="1083">1083</option>
	<option value="1106">1106</option>
	<option value="1109">1109</option>
	<option value="CUSTOM">CUSTOM</option>
</select>
% endif
</div>
<br />
% else:
<div class="rfid_brand">
<strong class="title2">
&nbsp;&nbsp;&nbsp;&nbsp;
</strong>
</div>
<br />
% endif
% endif