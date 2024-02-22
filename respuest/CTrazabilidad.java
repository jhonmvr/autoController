package com.erp.controller.gestor.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/gestor/web/CTrazabilidad")
public class CTrazabilidad {

    @Autowired
    private NTrazabilidad service;

    @PostMapping("/obtenerPorCriterios")
    public List<WebTrazabilidad> obtenerPorCriterios(@RequestBody FiltroTrazabilidadDTO criterios) {
        return service.obtenerPorCriterios(criterios);
    }
    @GetMapping("/getByReqId")
    public WebTrazabilidad getByReqId(@RequestParam("reqId") Long reqId) {
        return service.getByReqId(reqId);
    }
    @GetMapping("/getById")
    public WebTrazabilidad getById(@RequestParam("trzId") Long trzId) {
        return service.getById(trzId);
    }
    @PostMapping("/obtenerPedidosByFechaEnvio")
    public List<VwWebTrazabilidadPedidos> obtenerPedidosByFechaEnvio(@RequestBody Timestamp fechaEnvio) {
        return service.obtenerPedidosByFechaEnvio(fechaEnvio);
    }
    @PostMapping("/obtenerPedidosByFechaEntrega")
    public List<VwWebTrazabilidadPedidos> obtenerPedidosByFechaEntrega(@RequestBody Timestamp fechaEntrega) {
        return service.obtenerPedidosByFechaEntrega(fechaEntrega);
    }
    @PostMapping("/getVwVentasOnlineByIds")
    public List<VwWebVentasOnline> getVwVentasOnlineByIds(@RequestBody List<Long> trzIds) {
        return service.getVwVentasOnlineByIds(trzIds);
    }
    @GetMapping("/getByEdwId")
    public WebTrazabilidad getByEdwId(@RequestParam("edwId") Long edwId) {
        return service.getByEdwId(edwId);
    }
    @GetMapping("/getByTrzNumeroFactura")
    public WebTrazabilidad getByTrzNumeroFactura(@RequestParam("trzNumeroFactura") String trzNumeroFactura) {
        return service.getByTrzNumeroFactura(trzNumeroFactura);
    }
    @GetMapping("/getByDspId")
    public WebTrazabilidad getByDspId(@RequestParam("dspId") long dspId) {
        return service.getByDspId(dspId);
    }
}