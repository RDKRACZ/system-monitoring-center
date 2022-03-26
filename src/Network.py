#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Network:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkTab.ui")

        # Get GUI objects
        self.grid1401 = builder.get_object('grid1401')
        self.drawingarea1401 = builder.get_object('drawingarea1401')
        self.button1401 = builder.get_object('button1401')
        self.label1401 = builder.get_object('label1401')
        self.label1402 = builder.get_object('label1402')
        self.label1403 = builder.get_object('label1403')
        self.label1404 = builder.get_object('label1404')
        self.label1405 = builder.get_object('label1405')
        self.label1406 = builder.get_object('label1406')
        self.label1407 = builder.get_object('label1407')
        self.label1408 = builder.get_object('label1408')
        self.label1409 = builder.get_object('label1409')
        self.label1410 = builder.get_object('label1410')
        self.label1411 = builder.get_object('label1411')
        self.label1412 = builder.get_object('label1412')
        self.label1413 = builder.get_object('label1413')

        # Connect GUI signals
        self.button1401.connect("clicked", self.on_button1401_clicked)
        self.drawingarea1401.connect("draw", self.on_drawingarea1401_draw)

        # Run initial function
        self.network_initial_func()


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1401_clicked(self, widget):

        from NetworkMenu import NetworkMenu
        NetworkMenu.popover1401p.set_relative_to(widget)
        NetworkMenu.popover1401p.set_position(1)
        NetworkMenu.popover1401p.popup()


    # ----------------------- Called for drawing Network download/upload speed as line chart -----------------------
    def on_drawingarea1401_draw(self, widget, ctx):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        network_receive_speed = Performance.network_receive_speed[Performance.selected_network_card_number]
        network_send_speed = Performance.network_send_speed[Performance.selected_network_card_number]

        chart_line_color = Config.chart_line_color_network_speed_data
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

        chart1401_width = Gtk.Widget.get_allocated_width(widget)
        chart1401_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart1401_width, chart1401_height)
        ctx.fill()

        ctx.set_line_width(1)
        ctx.set_dash([4, 3])
        ctx.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            ctx.move_to(0, chart1401_height/4*(i+1))
            ctx.line_to(chart1401_width, chart1401_height/4*(i+1))
        for i in range(4):
            ctx.move_to(chart1401_width/5*(i+1), 0)
            ctx.line_to(chart1401_width/5*(i+1), chart1401_height)
        ctx.stroke()

        chart1401_y_limit = 1.1 * ((max(max(network_receive_speed), max(network_send_speed))) + 0.0000001)
        if Config.plot_network_download_speed == 1 and Config.plot_network_upload_speed == 0:
            chart1401_y_limit = 1.1 * (max(network_receive_speed) + 0.0000001)
        if Config.plot_network_download_speed == 0 and Config.plot_network_upload_speed == 1:
            chart1401_y_limit = 1.1 * (max(network_send_speed) + 0.0000001)

        # ---------- Start - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------
        data_unit_for_chart_y_limit = 0
        if Config.performance_network_speed_data_unit >= 8:
            data_unit_for_chart_y_limit = 8
        try:
            chart1401_y_limit_str = f'{self.performance_data_unit_converter_func(chart1401_y_limit, data_unit_for_chart_y_limit, 0)}/s'
        except NameError:
            return
        chart1401_y_limit_split = chart1401_y_limit_str.split(" ")
        chart1401_y_limit_float = float(chart1401_y_limit_split[0])
        number_of_digits = len(str(int(chart1401_y_limit_split[0])))
        multiple = 10 ** (number_of_digits - 1)
        number_to_get_next_multiple = chart1401_y_limit_float + (multiple - 0.0001)
        next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
        self.label1413.set_text(f'{next_multiple} {chart1401_y_limit_split[1]}')
        chart1401_y_limit = (chart1401_y_limit * next_multiple / (chart1401_y_limit_float + 0.0000001) + 0.0000001)
        # ---------- End - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------

        ctx.set_dash([], 0)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        ctx.rectangle(0, 0, chart1401_width, chart1401_height)
        ctx.stroke()

        if Config.plot_network_download_speed == 1:
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            ctx.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_receive_speed[0]/chart1401_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1401a = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1401a = (chart1401_height*network_receive_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_receive_speed[i]/chart1401_y_limit)
                ctx.rel_line_to(delta_x_chart1401a, -delta_y_chart1401a)

            ctx.rel_line_to(10, 0)
            ctx.rel_line_to(0, chart1401_height+10)
            ctx.rel_line_to(-(chart1401_width+20), 0)
            ctx.rel_line_to(0, -(chart1401_height+10))
            ctx.close_path()
            ctx.stroke()

        if Config.plot_network_upload_speed == 1:
            ctx.set_dash([3, 3])
            ctx.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_send_speed[0]/chart1401_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1401b = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1401b = (chart1401_height*network_send_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_send_speed[i]/chart1401_y_limit)
                ctx.rel_line_to(delta_x_chart1401b, -delta_y_chart1401b)

            ctx.rel_line_to(10, 0)
            ctx.rel_line_to(0, chart1401_height+10)
            ctx.rel_line_to(-(chart1401_width+20), 0)
            ctx.rel_line_to(0, -(chart1401_height+10))
            ctx.close_path()
            ctx.stroke()


    # ----------------------------------- Network - Initial Function -----------------------------------
    def network_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]

        # Get vendor and model names
        device_vendor_name = "-"
        device_model_name = "-"
        if selected_network_card != "lo":
            # Read device vendor and model ids by reading "modalias" file.
            with open("/sys/class/net/" + selected_network_card + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            # Determine device subtype.
            device_subtype, device_alias = modalias_output.split(":", 1)
            # Get device vendor and model ids and read "pci.ids" file if device subtype is "pci". Also trim "0000" characters by using [4:].
            if device_subtype == "pci":
                device_vendor_id = device_alias.split("v", 1)[-1].split("d", 1)[0].lower()[4:]
                device_model_id = device_alias.split("d", 1)[-1].split("sv", 1)[0].lower()[4:]
                # Read "pci.ids" file.
                with open("/usr/share/hwdata/pci.ids") as reader:
                    ids_file_output = reader.read()
            # Get device vendor and model ids and read "usb.ids" file if device subtype is "pci".
            if device_subtype == "usb":
                device_vendor_id = device_alias.split("v", 1)[-1].split("p", 1)[0].lower()
                device_model_id = device_alias.split("p", 1)[-1].split("d", 1)[0].lower()
                # Read "usb.ids" file by specifying encoding method. Because this file has some characters in different encoding method.
                with open("/usr/share/hwdata/usb.ids", encoding='ISO-8859-1') as reader:
                    ids_file_output = reader.read()
            # Search device vendor and model names in the pci.ids or usb.ids file.
            device_vendor_id = "\n" + device_vendor_id + "  "
            device_model_id = "\n\t" + device_model_id + "  "
            if device_vendor_id in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(device_vendor_id, 1)[1]
                device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0].strip()
                # "device name" information may not be present in the pci.ids file.
                if device_model_id in rest_of_the_ids_file_output:
                    rest_of_the_rest_of_the_ids_file_output = rest_of_the_ids_file_output.split(device_model_id, 1)[1]
                    device_model_name = rest_of_the_rest_of_the_ids_file_output.split("\n", 1)[0].strip()
                else:
                    device_model_name = f'[{_tr("Unknown")}]'
            else:
                device_vendor_name = f'[{_tr("Unknown")}]'
                device_model_name = f'[{_tr("Unknown")}]'
        network_card_device_model_name = f'{device_vendor_name} - {device_model_name}'
        # lo (Loopback Device) is a system device and it is not a physical device. It could not be found in "pci.ids" file.
        if selected_network_card == "lo":
            network_card_device_model_name = "Loopback Device"

        # Get connection_type
        if selected_network_card.startswith("en"):
            connection_type = _tr("Ethernet")
        elif selected_network_card.startswith("wl"):
            connection_type = _tr("Wi-Fi")
        else:
            connection_type = "-"

        # Get network_card_mac_address
        with open("/sys/class/net/" + selected_network_card + "/address") as reader:
            network_card_mac_address = reader.read().strip().upper()

        # Get network_address_ipv4, network_address_ipv6
        ip_output_lines = (subprocess.check_output(["ip", "a", "show", selected_network_card], shell=False)).decode().strip().split("\n")
        for line in ip_output_lines:
            if "inet " in line:
                network_address_ipv4 = line.split()[1].split("/")[0]
            if "inet6 " in line:
                network_address_ipv6 = line.split()[1].split("/")[0]
        if "network_address_ipv4" not in locals():
            network_address_ipv4 = "-"
        if "network_address_ipv6" not in locals():
            network_address_ipv6 = "-"


        # Set Network tab label texts by using information get
        self.label1401.set_text(network_card_device_model_name)
        self.label1402.set_text(selected_network_card)
        self.label1407.set_text(connection_type)
        self.label1410.set_text(network_address_ipv4)
        self.label1411.set_text(network_address_ipv6)
        self.label1412.set_text(network_card_mac_address)


    # ----------------------------------- Network - Initial Function -----------------------------------
    def network_loop_func(self):

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]

        # Run "disk_initial_func" if selected network card is changed since the last loop.
        try:
            if self.selected_network_card_prev != selected_network_card:
                self.network_initial_func()
        # Avoid errors if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_network_card_prev = selected_network_card

        network_receive_speed = Performance.network_receive_speed
        network_send_speed = Performance.network_send_speed
        network_receive_bytes = Performance.network_receive_bytes
        network_send_bytes = Performance.network_send_bytes

        performance_network_speed_data_precision = Config.performance_network_speed_data_precision
        performance_network_data_data_precision = Config.performance_network_data_data_precision
        performance_network_speed_data_unit = Config.performance_network_speed_data_unit
        performance_network_data_data_unit = Config.performance_network_data_data_unit

        self.drawingarea1401.queue_draw()

        # Get network_card_connected
        # Get the information of if network card is connected by usng "/sys/class/net/" file.
        with open("/sys/class/net/" + selected_network_card + "/operstate") as reader:
            network_info = reader.read().strip()
        if network_info == "up":
            network_card_connected = _tr("Yes")
        elif network_info == "down":
            network_card_connected = _tr("No")
        elif network_info == "unknown":
            network_card_connected = f'[{_tr("Unknown")}]'
        else:
            network_card_connected = network_info

        # Get network_ssid
        try:                                                                                      
            nmcli_output_lines = (subprocess.check_output(["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"], shell=False)).decode().strip().split("\n")
        # Avoid errors because Network Manager (which is required for running "nmcli" command) may not be installed on all systems (very rare).
        except FileNotFoundError:
            network_ssid = f'[{_tr("Unknown")}]'
        # Check if "nmcli_output_lines" value is get.
        if "nmcli_output_lines" in locals():
            for line in nmcli_output_lines:
                line_splitted = line.split(":")
                if selected_network_card == line_splitted[0]:
                    network_ssid = line_splitted[1].strip()
                    break
        # "network_ssid" value is get as "" if selected network card is not connected a Wi-Fi network.
        if network_ssid == "":
            network_ssid = "-"

        # Get network_signal_strength
        network_signal_strength = "-"
        # Translated value have to be used by using gettext constant. Not "Yes".
        if "wl" in selected_network_card and network_card_connected == _tr("Yes"):
            with open("/proc/net/wireless") as reader:
                proc_net_wireless_output_lines = reader.read().strip().split("\n")
            for line in proc_net_wireless_output_lines:
                line_splitted = line.split()
                if selected_network_card == line_splitted[0].split(":")[0]:
                    # "split(".")" is used in order to remove "." at the end of the signal value.
                    network_signal_strength = line_splitted[2].split(".")[0]
                    break


        # Set and update Network tab label texts by using information get
        self.label1403.set_text(f'{self.performance_data_unit_converter_func(network_receive_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
        self.label1404.set_text(f'{self.performance_data_unit_converter_func(network_send_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
        self.label1405.set_text(self.performance_data_unit_converter_func(network_receive_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
        self.label1406.set_text(self.performance_data_unit_converter_func(network_send_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
        self.label1408.set_text(f'{network_card_connected} - {network_ssid}')
        self.label1409.set_text(network_signal_strength)


# Generate object
Network = Network()

