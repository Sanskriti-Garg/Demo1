package com.wellsfargo.demo1.repository;

import com.wellsfargo.demo1.model.Subject;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SubjectRepository extends JpaRepository<Subject, String> {
}
