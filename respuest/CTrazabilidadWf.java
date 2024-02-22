package com.erp.controller.gestor.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/gestor/web/CTrazabilidadWf")
public class CTrazabilidadWf {

    @Autowired
    private NTrazabilidadWf service;

    @PostMapping("/saveOrUpdate")
    public void saveOrUpdate(@RequestBody WebTrazabilidadWf entity) {
        service.saveOrUpdate(entity);
    }
    @GetMapping("/getByTrzId")
    public List<WebTrazabilidadWf> getByTrzId(@RequestParam("trzId") Long trzId) {
        return service.getByTrzId(trzId);
    }
    @PostMapping("/getByTrzIdTipoProceso")
    public WebTrazabilidadWf getByTrzIdTipoProceso(@RequestParam("trzId") Long trzId, @RequestBody EnumTipoProcesoTrazabilidad trwTipoProceso) {
        return service.getByTrzIdTipoProceso(trzId, trwTipoProceso);
    }
    @PostMapping("/getByTrzIdTipoIdProcesoStatus")
    public WebTrazabilidadWf getByTrzIdTipoIdProcesoStatus(@RequestParam("trzId") Long trzId, @RequestBody EnumTipoProcesoTrazabilidad trwTipoProceso, @RequestParam("trwProcesoId") Long trwProcesoId, @RequestParam("status") long status) {
        return service.getByTrzIdTipoIdProcesoStatus(trzId, trwTipoProceso, trwProcesoId, status);
    }
}