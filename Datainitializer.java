package com.wellsfargo.orchestra.examples;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import com.wellsfargo.orchestra.examples.model.Student;
import com.wellsfargo.orchestra.examples.model.Subject;
import com.wellsfargo.orchestra.examples.repository.StudentRepository;
import com.wellsfargo.orchestra.examples.repository.SubjectRepository;

@Component
public class DataInitializer implements CommandLineRunner {

    private final StudentRepository studentRepository;
    private final SubjectRepository subjectRepository;

    @Autowired
    public DataInitializer(StudentRepository studentRepository, SubjectRepository subjectRepository) {
        this.studentRepository = studentRepository;
        this.subjectRepository = subjectRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        // Initialize subjects
        Subject subject1 = new Subject("MATH101", "Mathematics");
        Subject subject2 = new Subject("PHY101", "Physics");
        subjectRepository.save(subject1);
        subjectRepository.save(subject2);

        // Initialize students
        Student student1 = new Student("REG001", "John Doe", "MATH101");
        Student student2 = new Student("REG002", "Jane Smith", "PHY101");
        studentRepository.save(student1);
        studentRepository.save(student2);

        System.out.println("Data initialized successfully");
    }
}
