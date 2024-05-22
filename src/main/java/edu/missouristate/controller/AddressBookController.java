// Bertrand Rusanganwa

package edu.missouristate.controller;

import edu.missouristate.domain.Address;
import edu.missouristate.service.AddressService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpSession;
import java.util.List;

@Controller
public class AddressBookController {
    @Autowired
    AddressService addressService;



    @GetMapping("/addEditAddress")

    public String getAddEditAddress(Model model,
                                    Integer addressId, HttpSession session,

                                    @ModelAttribute("message") String message,

                                    @ModelAttribute("messageType") String messageType) {
        model.addAttribute("heading", "Add Contact");

        // If addressId is not null then we need to edit an address
        // as opposed to adding an address

        if (addressId != null) {
            // We need to get the Address from our database with this id

            Address address = addressService.getAddressById(addressId);


            // If the address from the database is not null, then we found

            // a valid address. Place it on the model. Otherwise, we need to

            // place a message in session to let the user know we could not

            // find the Address with that address Id

            if (address != null) {
                // Update the heading since we are editing a contact

                model.addAttribute("heading", "Edit Contact");
                model.addAttribute("address", address);
            }

            else {

                // We didn't find a valid address so we need to send a message

                session.setAttribute("message", "Sorry, unable to find a " +
                        " contact with that address ID.");
                session.setAttribute("messageType", "danger");
            }
        }
        return "addEditAddress";
    }
    @GetMapping("/")

    public String getIndex(Model model) {

        List<Address> addressList = addressService.getAddresses();

        model.addAttribute("addressList"
                , addressList);
        return "index";
    }

    @GetMapping("/deleteAddress")

    public String getDeleteAddress(Model model, HttpSession session,
                                   Integer addressId) {
        try {
            if (addressId != null) {
                addressService.deleteAddress(addressId);

                session.setAttribute("message", "Contact Record Deleted Successfully");

                session.setAttribute("messageType", "success");

            }

            else {
                // We didn't find a valid address to delete, so
                // we need to send a message
                session.setAttribute("message", "Sorry, unable to find a " + " contact with that address ID.");

                session.setAttribute("messageType", "danger");
            }
        }
        catch (Exception e) {
            // Set an error message on the session
            session.setAttribute("messageType", "danger");

            session.setAttribute("message", "There was an error processing your request. " + "Error = " + e.getMessage());
        }
        return "redirect:/";
    }


    @PostMapping("/addEditAddress")

    public String postAddEditAddress(HttpSession session, Address address) {
        try {
            // Set the message based on whether we have an addressId or not.

            String message = (address != null && address.getAddressId() != null) ?

                    "Contact Updated Successfully" : "Contact Added Successfully";

            // This is really cool! If we are missing the addressId on the address

            // then we are "adding" a new record. Hibernate knows and creates

            // the Insert statement when we call save(address). If the addressId is

            // not null then Hibernate knows and creates the Update statement when

            // we call save(address). Again, we do not need to write any SQL.

            // Hibernate builds all the SQL for us.

            addressService.saveAddress(address);

            // Set a success message on the session

            session.setAttribute("message", message);

            session.setAttribute("messageType", "success");

            return "redirect:/";
        }

        catch (Exception e) {
            // Set an error message on the session

            session.setAttribute("messageType", "danger");

            session.setAttribute("message", "There was an error processing your request. " + "Error = " + e.getMessage());

            return "redirect:/addEditAddress";
        }
    }
}