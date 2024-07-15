package com.wellsfargo.demo1.repository;

import com.wellsfargo.demo1.model.Student;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StudentRepository extends JpaRepository<Student, String> {
}
