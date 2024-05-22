// Bertrand Rusanganwa

package edu.missouristate.domain;


import javax.persistence.*;

@Entity
@Table(name="addresses")

public class Address {

    @Id

    @GeneratedValue(strategy = GenerationType.IDENTITY)

    @Column( name="address_id", columnDefinition="Integer")
    private Integer addressId;

    @Column( name="first_name", columnDefinition="VARCHAR(64)")
    private String firstName;

    @Column( name="last_name", columnDefinition="VARCHAR(64)")
    private String lastName;
    @Column( name="address_one", columnDefinition="VARCHAR(128)")
    private String addressOne;

    @Column( name="address_two", columnDefinition="VARCHAR(128)")
    private String addressTwo;

    @Column( name="city", columnDefinition="VARCHAR(64)")
    private String city;

    @Column( name="state", columnDefinition="VARCHAR(64)")
    private String state;

    @Column( name="zip", columnDefinition="VARCHAR(10)")
    private String zip;

    public Integer getAddressId() {
        return addressId;
    }

    public void setAddressId(Integer addressId) {
        this.addressId = addressId;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getAddressOne() {
        return addressOne;
    }

    public void setAddressOne(String addressOne) {
        this.addressOne = addressOne;
    }

    public String getAddressTwo() {
        return addressTwo;
    }

    public void setAddressTwo(String addressTwo) {
        this.addressTwo = addressTwo;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getZip() {
        return zip;
    }

    public void setZip(String zip) {
        this.zip = zip;
    }
}