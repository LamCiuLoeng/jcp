% if rfid == "YES":
<div class="rfid_brand">
 PLEASE SELECT ORDER OPTION:
&nbsp;&nbsp;
<select name="private_brand" class="rfid_selection">
	<option value="">Please select...</option>
	<option value="0-${rfid_mapping_code}-Ticket-RFID">RFID and Ticket</option>
	<option value="1-${rfid_mapping_code}-Ticket">Ticket Only</option>
	<option value="2-${rfid_mapping_code}-RFID">RFID Only</option>
</select>
% if msgHeader.details[0].Brand_Typ == 'N':
&nbsp;&nbsp;&nbsp;&nbsp;
Please select the ticket stock number:
&nbsp;&nbsp;
<select name="national_brand" class="national_selection">
	<option value=""></option>
	<option value="0214">0214</option>
	<option value="0215">0215</option>
	<option value="0802">0802</option>
	<option value="0803">0803</option>
	<option value="0804">0804</option>
	<option value="0805">0805</option>
	<option value="0807">0807</option>
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
% endif
% if rfid == "NO" and combo_item and combo_flag == True:
<div class="rfid_brand">
PLEASE SELECT THE ORDER OPTION:
&nbsp;&nbsp;
<select name="combo_selection" class="combo_selection">
	<option value="">Please select...</option>
	<option value="1-${combo_item.packaging_code}-Ticket">Ticket only</option>
	<option value="0-${combo_item.packaging_code}-Ticket-Barcode">Ticket and Barcode</option>
	<option value="2-${combo_item.packaging_code}-Barcode">Barcode only</option>
</select>
</div>
% endif
<%doc>
% if sticker_code:
<div class="rfid_brand">
PLEASE SELECT THE ORDER OPTION:
&nbsp;&nbsp;
<select name="combo_selection" class="sticker_selection">
	<option value="">Please select...</option>
	<option value="0-${sticker_code}-ALL">ALL</option>
	<option value="1-${sticker_code}-Ticket-Sticker">Ticket/RFID and Sticker</option>
	<option value="2-${sticker_code}-Barcode">Sticker only</option>
</select>
</div>
% endif
</%doc>