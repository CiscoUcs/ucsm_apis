# API Conventions

#### API Naming conventions:

    - API must start with the name of the module.
    - noun_verb format.
    - `snmp_enable` better than `enable_snmp`
    - This allows for better API discoverability when using editor autocompletion.

#### required APIs per module

    - module_create/module_add/module_enable
        - Arguments:
            - UcsHandle
            - Naming and RW properties should be specified as explicit arguments
            - Naming property should be a mandatory argument. No default values
            - RW props should not be mandatory and have `None` as the default value.
            - do not include `status` in arguments even though it is a RW
              property.
            - have **kwargs as the last argument. This allows for
              extensibility.
        - API logic:
            - always include `set_prop_multiple(**kwargs)` in the function
              implementation
        - Returns: Created MO

    - module_delete/module_remove/module_disable
        - Arguments:
            - UcsHandle
            - Naming properties as mandatory argument(s)
        - Returns:
            - Nothing

    - module_get/module_query

    - module_modify(where applicable)
        - This method is ideally designed for usage from configuration management tools
        - Arguments:
            - Ucshandle
            - Naming Peroperties as mandatory parameters
            - RW props **kwargs

    - module_exists:
        - This method is ideally designed for usage from configuration management tools
        - Arguments:
            - Ucshandle
            - Naming properties as manadatory parameters
            - **kwargs
        - API Logic
            - always use `mo.check_prop_match(**kwargs)`
        - Returns: (boolean, server_copy of mo)

