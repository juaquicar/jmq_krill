from jmq_krill.krill_api import PyJMQKrill, APIError


def main():
    host = "https://host.es"
    username = "username"
    password = "password"
    client = PyJMQKrill(host, username, password)

    try:
        token = client.login()
        print(f"Authenticated, token: {token}")

        # Ejemplo: obtener CPEs por topología
        # topology = "3a44340d-1996-4555-9093-5685af073056"
        # cpes = client.get_cpes_by_gen_equipos(topology)
        # print(f"CPEs en '{topology}':", cpes)

        # Ejemplo: información detallada de un CPE
        # cpe_id = 238
        # info = client.get_cpe_info(cpe_id)
        # print(f"Info de CPE '{cpe_id}':", info)

        # Ejemplo: estado de ONUs por OLT
        olt_name = "oltCEEIM"
        frame, slot, port = '0', '05', '15'
        onus_status = client.get_cpes_by_olt(olt_name, frame, slot, port)
        print(f"Estado de ONUs en OLT '{olt_name}':", onus_status)

        # Ejemplo: obtener todos los CPEs de monitoring
        # all_cpes = client.get_cpes_monitoring()
        # print(f"Total CPEs monitoreados: {len(all_cpes)}")

    except APIError as e:
        print("APIError:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
