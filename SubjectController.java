package com.wellsfargo.demo1.controller;

import com.wellsfargo.demo1.model.Subject;
import com.wellsfargo.demo1.repository.SubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/subjects")
public class SubjectController {

    @Autowired
    private SubjectRepository subjectRepository;

    @GetMapping
    public List<Subject> getAllSubjects() {
        return subjectRepository.findAll();
    }

    @PostMapping
    public Subject createSubject(@RequestBody Subject subject) {
        return subjectRepository.save(subject);
    }

    @GetMapping("/{id}")
    public Subject getSubjectById(@PathVariable String id) {
        return subjectRepository.findById(id).orElse(null);
    }

    @PutMapping("/{id}")
    public Subject updateSubject(@PathVariable String id, @RequestBody Subject subjectDetails) {
        Subject subject = subjectRepository.findById(id).orElse(null);
        if (subject != null) {
            subject.setSubjectName(subjectDetails.getSubjectName());
            return subjectRepository.save(subject);
        }
        return null;
    }

    @DeleteMapping("/{id}")
    public void deleteSubject(@PathVariable String id) {
        subjectRepository.deleteById(id);
    }
}
