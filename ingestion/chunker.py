# ingestion/chunker.py

from typing import List, Dict
import re


class CodeChunker:

    def create_chunks(
        self,
        parsed_file: Dict
    ) -> List[Dict]:

        chunks = []

        chunks.append(
            self._create_file_chunk(
                parsed_file
            )
        )

        for component in parsed_file.get(
            "components",
            []
        ):
            chunks.append(
                self._create_component_chunk(
                    component,
                    parsed_file
                )
            )

        for function in parsed_file.get(
            "functions",
            []
        ):
            chunks.append(
                self._create_function_chunk(
                    function,
                    parsed_file
                )
            )

        for api in parsed_file.get(
            "api_calls",
            []
        ):
            chunks.append(
                self._create_api_chunk(
                    api,
                    parsed_file
                )
            )

        return chunks

    # -----------------------------------
    # FILE CHUNK
    # -----------------------------------

    def _create_file_chunk(
        self,
        parsed_file
    ):

        return {

            "type": "file",

            "name":
                parsed_file["file_name"],

            "path":
                parsed_file["path"],

            "content":
                self._build_file_summary(
                    parsed_file
                ),

            "metadata": {

                "components":
                    parsed_file["components"],

                "functions":
                    parsed_file["functions"],

                "hooks":
                    parsed_file["hooks"],

                "imports":
                    parsed_file["imports"],

                "api_calls":
                    parsed_file["api_calls"]
            }
        }

    # -----------------------------------
    # COMPONENT CHUNK
    # -----------------------------------

    def _create_component_chunk(
        self,
        component,
        parsed_file
    ):

        component_code = (
            self.extract_component_code(
                component,
                parsed_file["code"]
            )
        )

        return {

            "type":
                "component",

            "name":
                component,

            "path":
                parsed_file["path"],

            "content":
                component_code,

            "metadata": {

                "file":
                    parsed_file["file_name"],

                "hooks":
                    parsed_file["hooks"],

                "imports":
                    parsed_file["imports"]
            }
        }



    # -----------------------------------
    # FUNCTION CHUNK
    # -----------------------------------

    def _create_function_chunk(
        self,
        function,
        parsed_file
    ):

        # Use full file code temporarily
        function_code = parsed_file["code"]
        if function == "loginApi":
            print(function_code)

        function_calls = [
            fn
            for fn in self.extract_function_calls(
                function_code
            )
            if fn != function
        ]

        return {

            "type": "function",

            "name": function,

            "path": parsed_file["path"],

            "content": function_code,

            "metadata":
            {
                "file":
                    parsed_file["file_name"],

                "components":
                    parsed_file["components"],

                "service_calls":
                    parsed_file["service_calls"],

                "api_calls":
                    self.extract_api_calls(function_code),

                "function_calls":
                    function_calls
            }
        }

    def extract_function_calls(
        self,
        code
    ):

        matches = re.findall(
            r'(?<!\.)\b([a-z][A-Za-z0-9_]*)\s*\(',
            code
        )

        ignore = {
            "if",
            "for",
            "while",
            "switch",
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

    def _create_api_chunk(
        self,
        api,
        parsed_file
    ):

        return {

            "type":
                "api",

            "name":
                api,

            "path":
                parsed_file["path"],

            "content":
                api,

            "metadata": {

                "file":
                    parsed_file["file_name"]
            }
        }

    # -----------------------------------
    # FILE SUMMARY
    # -----------------------------------

    def _build_file_summary(
        self,
        parsed_file
    ):

        return f"""
File:
{parsed_file['file_name']}

Components:
{', '.join(parsed_file['components'])}

Functions:
{', '.join(parsed_file['functions'])}

Hooks:
{', '.join(parsed_file['hooks'])}

Imports:
{', '.join(parsed_file['imports'])}

APIs:
{', '.join(parsed_file['api_calls'])}
"""

    # -----------------------------------
    # EXTRACT COMPONENT CODE
    # -----------------------------------

    def extract_component_code(
        self,
        component_name,
        code
    ):

        pattern = (
            rf'function\s+{component_name}'
            rf'[\s\S]*?return'
            rf'[\s\S]*?\);'
        )

        match = re.search(
            pattern,
            code
        )

        if match:
            return match.group(0)

        return ""

    # -----------------------------------
    # EXTRACT FUNCTION CODE
    # -----------------------------------

    def extract_function_code(
        self,
        function_name,
        code
    ):

        patterns = [

            rf'const\s+{function_name}\s*=\s*.*?\=\>\s*\{{[\s\S]*?\n\}};',

            rf'function\s+{function_name}\s*\([\s\S]*?\n\}}',

            rf'static\s+async\s+{function_name}\s*\([\s\S]*?\n\s*\}}',

            rf'static\s+{function_name}\s*\([\s\S]*?\n\s*\}}'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                code,
                re.MULTILINE
            )

            if match:
                return match.group(0)

        return ""

    def extract_api_calls(
        self,
        code
    ):

        matches = []

        patterns = [

            r'axios\.get\([\'"](.+?)[\'"]',
            r'axios\.post\([\'"](.+?)[\'"]',
            r'axios\.put\([\'"](.+?)[\'"]',
            r'axios\.delete\([\'"](.+?)[\'"]',
            r'fetch\([\'"](.+?)[\'"]'
        ]

        for pattern in patterns:

            matches.extend(
                re.findall(
                    pattern,
                    code
                )
            )

        return list(set(matches))        