import pandapower as pp


def run():
    # create empty net
    net = pp.create_empty_network()

    # create buses
    b1 = pp.create_bus(net, vn_kv=20.0, name="Bus 1")
    b2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
    b3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")
    b4 = pp.create_bus(net, vn_kv=0.4, name="Bus 4")  # new bus
    b5 = pp.create_bus(net, vn_kv=0.4, name="Bus 5")  # new bus for PV plant
    b6 = pp.create_bus(net, vn_kv=0.4, name="Bus 6")  # new bus for external connection

    # create bus elements
    pp.create_ext_grid(net, bus=b1, vm_pu=1.02, name="Grid Connection")
    pp.create_load(net, bus=b3, p_mw=0.1, q_mvar=0.05, name="Load")

    # create branch elements
    tid1 = pp.create_transformer(
        net, hv_bus=b1, lv_bus=b2, std_type="0.4 MVA 20/0.4 kV", name="Trafo 1"
    )
    pp.create_line(
        net, from_bus=b2, to_bus=b3, length_km=0.1, name="Line", std_type="NAYY 4x50 SE"
    )
    tid2 = pp.create_transformer(
        net, hv_bus=b1, lv_bus=b4, std_type="0.4 MVA 20/0.4 kV", name="Trafo 2"
    )  # new transformer

    # add load, PV plant, and external connection node on low voltage side of new transformer
    pp.create_load(net, bus=b4, p_mw=0.2, q_mvar=0.1, name="Load 2")
    pp.create_gen(net, bus=b4, p_mw=5, q_mvar=50, name="PV Plant")
    for i in range(5):
        pp.create_sgen(net, b5, p_mw=1, q_mvar=0.1, name=f"PV {i+1}")
    pp.create_ext_grid(net, bus=b6, vm_pu=1.02, name="External Connection")

    def run_simulation():
        pp.runpp(net)
        return net

    net = run_simulation()
    results = {"loads": {}, "generators": {}, "external_grid": {}}
    # extract active power, reactive power, and node name for load element
    for element in net.load.index:
        p_mw = net.res_load.loc[element, "p_mw"]
        q_mvar = net.res_load.loc[element, "q_mvar"]
        node_name = net.load.loc[element, "name"]
        node_dict = (f"{p_mw} MW", f"{q_mvar} Mvar")
        results["loads"][node_name] = node_dict

    # extract active power, reactive power, and node name for generator element
    for element in net.gen.index:
        p_mw = net.res_gen.loc[element, "p_mw"]
        q_mvar = net.res_gen.loc[element, "q_mvar"]
        node_name = net.gen.loc[element, "name"]
        node_dict = (f"{p_mw} MW", f"{q_mvar} Mvar")
        results["generators"][node_name] = node_dict

    # extract active power, reactive power, and node name for external grid element
    for element in net.ext_grid.index:
        p_mw = net.res_ext_grid.loc[element, "p_mw"]
        q_mvar = net.res_ext_grid.loc[element, "q_mvar"]
        node_name = net.ext_grid.loc[element, "name"]
        node_dict = (f"{p_mw} MW", f"{q_mvar} Mvar")
        results["external_grid"][node_name] = node_dict
    return results
