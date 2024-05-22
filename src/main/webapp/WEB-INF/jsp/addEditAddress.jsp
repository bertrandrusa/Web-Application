<!-- Bertrand, Rusanganwa  -->

<%@ include file="include.jsp" %>
<!DOCTYPE html>
<html>

<head>
    <jsp:include page="head.jsp"/>
    <title> </title>
</head>

<body>

<div class="container">

    <div class="row">

        <div class="col-12">

            <h1 class="mt-3 mb-4">${heading}</h1>

            <jsp:include page="message.jsp"/>
        </div>
    </div>
</div>

<form method="post" action="<%=request.getContextPath()%>/addEditAddress">

    <input type="hidden" id="addressId" name="addressId" value="${address.addressId}" />

    <div class="row">
        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="firstName"><b>First Name</b></label>

            <input class="form-control" name="firstName" id="firstName"

                   placeholder="First Name" value="${address.firstName}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="lastName"><b>Last Name</b></label>

            <input class="form-control" name="lastName" id="lastName"

                   placeholder="Last Name" value="${address.lastName}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="addressOne"><b>Address</b></label>

            <input class="form-control" name="addressOne" id="addressOne"

                   placeholder="Address" value="${address.addressOne}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="addressTwo"><b>Address Two</b></label>

            <input class="form-control" name="addressTwo" id="addressTwo"

                   placeholder="Address Two" value="${address.addressTwo}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="city"><b>City</b></label>

            <input class="form-control" name="city" id="city"

                   placeholder="City" value="${address.city}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="state"><b>State</b></label>

            <input class="form-control" name="state" id="state"

                   placeholder="State" value="${address.state}">
        </div>


        <div class="col-12 col-sm-6 col-md-4 form-group">

            <label for="zip"><b>Address Two</b></label>

            <input class="form-control" name="zip" id="zip"

                   placeholder="Zip" value="${address.zip}">
        </div>


    </div>
    <button id="btnSubmit" type="submit" class="btn btn-primary">Submit</button>
</form>

</body>

</html>