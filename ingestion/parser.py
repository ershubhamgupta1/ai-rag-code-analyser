# ingestion/parser.py

import re


class ReactParser:

    IGNORE_FUNCTIONS = {
        "return",
        "async",
        "await",
        "useState",
        "useEffect",
        "useMemo",
        "useCallback",
        "useRef",
        "useContext"
    }

    def parse_file(self, file_data: dict):

        code = file_data["content"]

        components = self.extract_components(
            code
        )

        functions = self.extract_functions(
            code,
            components
        )

        return {
            "file_name": file_data["file_name"],
            "path": file_data["path"],
            "components": components,
            "functions": functions,
            "hooks": self.extract_hooks(code),
            "custom_hooks": self.extract_custom_hooks(code),
            "imports": self.extract_imports(code),
            "third_party_libs": self.extract_third_party_libs(code),
            "api_calls": self.extract_api_calls(code),
            "service_calls": self.extract_service_calls(code),
            "function_calls": self.extract_function_calls(code),
            "navigation_calls": self.extract_navigation_calls(code),
            "code": code
        }
    # ----------------------------------
    # Components
    # ----------------------------------

    def extract_components(self, code):

        components = []

        patterns = [

            # function Login(){}
            r'function\s+([A-Z][A-Za-z0-9_]*)',

            # const Login = () => {}
            r'const\s+([A-Z][A-Za-z0-9_]*)\s*=\s*\(',

            # const Login = React.memo(...)
            r'const\s+([A-Z][A-Za-z0-9_]*)\s*=\s*React\.memo'
        ]

        for pattern in patterns:

            components.extend(
                re.findall(
                    pattern,
                    code
                )
            )

        return sorted(
            list(set(components))
        )

    # ----------------------------------
    # Functions
    # ----------------------------------
    def extract_functions(
        self,
        code,
        components=None
    ):

        functions = []

        patterns = [

            # function handleSubmit(){}
            r'function\s+([a-z][A-Za-z0-9_]*)',

            # const handleSubmit = async () => {}
            r'const\s+([a-z][A-Za-z0-9_]*)\s*=\s*async',

            # const handleSubmit = () => {}
            r'const\s+([a-z][A-Za-z0-9_]*)\s*=\s*\(',

            # static async login()
            r'static\s+async\s+([a-z][A-Za-z0-9_]*)\s*\(',

            # static login()
            r'static\s+([a-z][A-Za-z0-9_]*)\s*\('
        ]

        for pattern in patterns:

            matches = re.findall(
                pattern,
                code
            )

            functions.extend(matches)

        functions = list(
            set(functions)
        )

        if components:

            functions = [
                fn
                for fn in functions
                if fn not in components
            ]

        functions = [
            fn
            for fn in functions
            if fn not in self.IGNORE_FUNCTIONS
        ]

        return sorted(functions)
    # ----------------------------------
    # React Hooks
    # ----------------------------------

    def extract_hooks(self, code):

        return sorted(
            list(
                set(
                    re.findall(
                        r'(use[A-Z][A-Za-z0-9_]*)',
                        code
                    )
                )
            )
        )

    # ----------------------------------
    # Custom Hooks
    # ----------------------------------

    def extract_custom_hooks(self, code):

        hooks = []

        hooks.extend(
            re.findall(
                r'function\s+(use[A-Z][A-Za-z0-9_]*)',
                code
            )
        )

        hooks.extend(
            re.findall(
                r'const\s+(use[A-Z][A-Za-z0-9_]*)',
                code
            )
        )

        return sorted(
            list(set(hooks))
        )

    # ----------------------------------
    # Imports
    # ----------------------------------

    def extract_imports(self, code):

        return re.findall(
            r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
            code
        )

    # ----------------------------------
    # Third Party Libraries
    # ----------------------------------

    def extract_third_party_libs(self, code):

        imports = self.extract_imports(
            code
        )

        return sorted(
            [
                item
                for item in imports
                if not item.startswith(".")
            ]
        )

    # ----------------------------------
    # API Calls
    # ----------------------------------

    def extract_api_calls(self, code):

        api_calls = []

        patterns = [

            r'axios\.get\([\'"](.+?)[\'"]',
            r'axios\.post\([\'"](.+?)[\'"]',
            r'axios\.put\([\'"](.+?)[\'"]',
            r'axios\.delete\([\'"](.+?)[\'"]',

            r'fetch\([\'"](.+?)[\'"]'
        ]

        for pattern in patterns:

            api_calls.extend(
                re.findall(
                    pattern,
                    code
                )
            )

        return sorted(
            list(set(api_calls))
        )

    # ----------------------------------
    # Service Calls
    # ----------------------------------

    def extract_service_calls(self, code):

        matches = re.findall(
            r'([A-Z][A-Za-z0-9_]*)\.([a-zA-Z0-9_]+)\(',
            code
        )

        return sorted(
            list(
                set(
                    [
                        method
                        for _, method
                        in matches
                    ]
                )
            )
        )
    # ----------------------------------
    # Navigation
    # ----------------------------------

    def extract_navigation_calls(self, code):

        routes = []

        routes.extend(
            re.findall(
                r'navigate\([\'"](.+?)[\'"]',
                code
            )
        )

        routes.extend(
            re.findall(
                r'to=[\'"](.+?)[\'"]',
                code
            )
        )

        return sorted(
            list(set(routes))
        )

    def extract_function_calls(self, code):

        matches = re.findall(
            r'([a-z][A-Za-z0-9_]*)\s*\(',
            code
        )

        ignore = {
            "if",
            "for",
            "while",
            "switch",
            "return",
            "useState",
            "useEffect",
            "useMemo",
            "useCallback",
            "useRef",
            "useContext"
        }

        return sorted(
            list(
                set(
                    [
                        fn
                        for fn in matches
                        if fn not in ignore
                    ]
                )
            )
        )