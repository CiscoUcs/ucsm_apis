# API Conventions

#### API Naming conventions:

    - API must start with the name of the module.
    - noun_verb format.
    - `snmp_enable` better than `enable_snmp`
    - This allows for better API discoverability when using editor autocompletion.

#### required APIs per module

    - module_create/module_add/module_enable
        - Arguments: Naming and RW properties should be specified as explicit arguments
        - Returns: Created MO

    - module_delete/module_remove/module_disable

    - module_modify(where applicable)
        - This method is ideally designed for usage from configuration management tools
        - Arguments: only takes Naming props and kwargs. No need to specify RW props explicitly.

    - module_exists:
        - This method is ideally designed for usage from configuration management tools
        - Gets a MO(s) as input to compare against server state. Intention is to check if the supplied MO(s) exist on the server. The supplied MO may have populated only some attribute values. These attribute values must also be compared with the server copy of the MO. False should be returned if the MO does not exist on the server or any of the populated property values do not match the supplied client copy.
        - Returns: (boolean, server_copy of mo)

