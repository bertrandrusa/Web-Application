// Bertrand Rusanganwa

package edu.missouristate.service;

import edu.missouristate.domain.Address;

import edu.missouristate.repository.AddressRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.List;
import java.util.Optional;

@Service
public class AddressService {
    @Autowired
    AddressRepository addressRepo;
    public List<Address> getAddresses() {
        return (List<Address>) addressRepo.findAll();}

    @Transactional
    public void saveAddress(Address address) {
        addressRepo.save(address);
    }

    public Address getAddressById(Integer addressId) {
        Optional<Address> addressOptional = addressRepo.findById(addressId);
        return addressOptional.isPresent() ? addressOptional.get() : null;
    }

    @Transactional
    public void deleteAddress(Integer addressId) {
        addressRepo.deleteById(addressId);
    }
}