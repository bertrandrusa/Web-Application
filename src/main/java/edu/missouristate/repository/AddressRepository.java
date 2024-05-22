// Bertrand Rusanganwa


package edu.missouristate.repository;
import edu.missouristate.domain.Address;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface AddressRepository extends CrudRepository<Address, Integer> {
}