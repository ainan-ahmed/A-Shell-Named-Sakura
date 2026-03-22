#!/usr/bin/env python3
"""Compile SCSS to CSS for GTK application."""

import sys
import sass


def main():
    if len(sys.argv) != 3:
        print("Usage: compile_scss.py <input.scss> <output.css>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Compile SCSS to CSS
    css = sass.compile(filename=input_file, output_style="expanded")

    # Replace escaped @ symbols with actual @ for GTK theme variables
    # SCSS uses \@ to escape @ symbols, we need to convert them back
    css = css.replace(r"\@", "@")

    # Remove charset declaration (GTK doesn't need it)
    css = css.replace('@charset "UTF-8";', "")

    # Write output
    with open(output_file, "w") as f:
        f.write(css)

    print(f"Compiled {input_file} -> {output_file}")


if __name__ == "__main__":
    main()
