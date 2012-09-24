<%@ Language=VBScript%> 
<%Option Explicit%>
<%
'dim objNewMail
Dim param
Dim Elem
Dim sText

sText = "<?xml version=""1.0"" encoding=""windows-1255""?> " & vbcrlf & "<vform>" & vbcrlf
set param = Request.Form
for each elem in param
    if elem<>"x" AND elem<>"y" AND elem<>"sender" then
        sText = sText & "<" & elem & ">" & replace(param(elem),"""","&quot;") & "</" & elem & ">" & vbcrlf
    end if
Next
sText = sText & "</vform>"%>
<% 
dim fs, f, namef
namef = "c:\data\forms\d\" & day(now) & month(now) & year(now) & Hour(now) & minute(now) & second(now) & ".XML"
set fs=Server.CreateObject("Scripting.FileSystemObject") 
set f=fs.OpenTextFile(namef,8,true)
f.WriteLine(sText)
f.Close
set f=nothing
set fs=nothing
%>


<!-- 
    METADATA 
    TYPE="typelib" 
    UUID="CD000000-8B95-11D1-82DB-00C04FB1625D"  
    NAME="CDO for Windows 2000 Library" 
-->
<%'response.redirect("thanks.asp")
'on error resume next
'dim results
'results=0
'Dim objMail
'Set objMail = Server.CreateObject("CDO.Message")
'SmtpPort = 25
'objMail.BodyPart.Charset = "windows-1255"
'objMail.HTMLBodyPart.charset = "Windows-1255"
'objMail.MIMEFormatted = true
'objMail.Subject=EMailSubject
'objMail.From= "טופס מעומד להתנדבות"
'objMail.To= "marcus.ben@gmail.com"
'objMail.HTMLBody = sText
'objMail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
'objMail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") = "sout.zahav.net.il"
'objMail.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/mailheader/content-type") = "text/html; charset=""windows-1255""" 'text/html
'objMail.Configuration.Fields.Item(cdoSMTPServerPort) = "25"
'objMail.Configuration.Fields.Item(cdoSendUserName) = "ruacht_2"
'objMail.Configuration.Fields.Item(cdoSendPassword) = "szqcm"
'objMail.Configuration.Fields.Item("urn:schemas:mailheader:content-type") = "text/html;charset=""windows-1255"""
'objMail.Configuration.Fields.Update
'objMail.Send
'set objMail = nothing
'results=err.number
'SendMail=results
'response.redirect("http://www.ynet.co.il/home/0,7340,L-3565,00.html")
%>
<html>
<body>
<%response.redirect("savionend.asp")%>
	<script language="javascript">
		<%=window%>.location.href = '<%=addr%>';
	</script>
<%end if%>
</body>
</html>