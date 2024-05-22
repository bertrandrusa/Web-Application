<!-- Bertrand, Rusanganwa  -->

<%@ page import="static java.awt.SystemColor.text" %>
<%
    try {
        // Grab message and message type from session and assign to variables.
        String message = (String)request.getSession().getAttribute("message");

        String messageType = (String)request.getSession().getAttribute("messageType");

        message = (message == null) ? "" : message; // if message is null, set it to the empty string

        messageType = (messageType == null) ? "" : messageType;

        if (message.length() > 0 && messageType.length() > 0) {
            // Check if messageType is success or danger

            boolean success = "success".equalsIgnoreCase(messageType);

            boolean danger = "danger".equalsIgnoreCase(messageType);

            if (success || danger) {
                // Build proper fontawesome icon

                String icon = (success) ? "fa-check-circle" : "fa-times-circle";

                // Build the div to display an error message or success message
                out.write("<div id='messages' class='border border- "+messageType+" p-1 mb-1 mt-1rounded text-"+messageType+"'>\n");

                out.write(" <i class='fa "+icon+" mr-3'></i>\n");

                out.write(message + "\n");

                out.write(" <span id='closeMessage' class='float-right pr-2'\n");

                out.write("" +"onclick=\"document.getElementById('messages').style.display='none'\">\n");

                out.write(" &times;\n");

                out.write(" </span>\n");

                out.write("</div>\n");
            }
        }
    } catch (Exception e) {

        e.printStackTrace();
    }
    finally {
        // Remove attributes from session since we are done with them

        request.getSession().removeAttribute("message");

        request.getSession().removeAttribute("messageType");
    }
%>