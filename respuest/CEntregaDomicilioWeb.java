package com.erp.controller.gestor.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/gestor/web/CEntregaDomicilioWeb")
public class CEntregaDomicilioWeb {

    @Autowired
    private NEntregaDomicilioWeb service;

    @GetMapping("/getByTrzId")
    public WebEntregaDomicilio getByTrzId(@RequestParam("trzId") long trzId) {
        return service.getByTrzId(trzId);
    }
}