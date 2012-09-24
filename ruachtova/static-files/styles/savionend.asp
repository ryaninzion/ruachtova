<!--#include file="DANA-parva.asp" -->
<%	
Dim param
Dim Elem, ID
set param = request.form
call AddXref(param, request("id"))
%>
<head>
<META HTTP-EQUIV ="Content-Type" content="text/html; charset=windows-1255" />
<!-- #include file="Include/urchincode.asp" --></head>
<table align="center" width="408" cellspacing="0" cellpadding="0" border="0">
	<tr>
		<td height="31" valign="bottom">
			<img src="topline.gif" width="100%" height="100%" />
		</td>
	</tr>
	<tr>
		<td style="font-family:arial;font-size:14px;padding:8px" dir="rtl" height="150" bgcolor="#E9EDF2" valign="top">
			פנייתך נקלטה במערכת "רוח טובה", <br />
			תודה
		</td>
	</tr>
	<tr>
		<td height="31">
			<img src="bottomline.gif" width="100%" height="100%" />
		</td>
	</tr>
</table>