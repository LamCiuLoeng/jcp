<%inherit file="ordering.templates.master"/>

<%!
	from tg.flash import get_flash,get_status
	from repoze.what.predicates import not_anonymous,in_group,has_permission,has_any_permission
%>

<%def name="extTitle()">r-pac - Master</%def>

<div class="main-div">
	<div id="main-content">
		% if in_group("Admin"):
		<div class="block">
			<a href="/country/index"><img src="/images/country.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/country/index">Country</a></p>
			<div class="block-content">The module is the master of the "JCPenney Country" .</div>
		</div>
		
		<div class="block">
			<a href="/contact/index"><img src="/images/contact.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/contact/index">Contact</a></p>
			<div class="block-content">The module is the master of the "JCPenney contact" .</div>
		</div>
		% if in_group("Admin") or in_group("AE"):
		<div class="block">
			<a href="/billto/index"><img src="/images/billto.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/billto/index">BillTo</a></p>
			<div class="block-content">The module is the master of the "JCPenney BillTo" .</div>
		</div>
		
		<div class="block">
			<a href="/shipto/index"><img src="/images/shipto.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/shipto/index">ShipTo</a></p>
			<div class="block-content">The module is the master of the "JCPenney ShipTo" .</div>
		</div>
		% endif
		<div class="block">
			<a href="/countrycode/index"><img src="/images/countrycode.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/countrycode/index">Country Code</a></p>
			<div class="block-content">The module is the master of the "JCPenney Country Code" .</div>
		</div>
		% endif
		<div class="block">
			<a href="/iteminfo/index"><img src="/images/iteminfo.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/iteminfo/index">Item Info</a></p>
			<div class="block-content">The module is the master of the "JCPenney Item Info" .</div>
		</div>
		% if in_group("Admin") or in_group("AE"):
		<div class="block">
			<a href="/customer/index"><img src="/images/customer.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/customer/index">Customer</a></p>
			<div class="block-content">The module is the master of the "JCPenney Customer" .</div>
		</div>
		<div class="block">
			<a href="/specialvalue/index"><img src="/images/specialvalue.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/specialvalue/index">Special Value</a></p>
			<div class="block-content">The module is the master of the "JCPenney Special Value" .</div>
		</div>
		<!--div class="block">
			<a href="/rfidmapping/index"><img src="/images/size.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/rfidmapping/index">RFID Mapping</a></p>
			<div class="block-content">The module is the master of the "JCPenney RFID Mapping" .</div>
		</div>
		<div class="block">
			<a href="/combomapping/index"><img src="/images/billto.jpg" width="55" height="55" alt="" /></a>
			<p><a href="/combomapping/index">Combo Mapping</a></p>
			<div class="block-content">The module is the master of the "JCPenney Combo Mapping" .</div>
		</div-->
		% endif
	</div>
</div>
