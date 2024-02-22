package com.erp.controller.gestor.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/gestor/web/CTrazabilidadDetalle")
public class CTrazabilidadDetalle {

    @Autowired
    private NTrazabilidadDetalle service;

    @GetMapping("/getDetalleByTrzId")
    public List<WebTrazabilidadDetalle> getDetalleByTrzId(@RequestParam("trzId") Long trzId) {
        return service.getDetalleByTrzId(trzId);
    }
}