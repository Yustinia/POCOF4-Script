#!/bin/bash

PORT_dir="$(pwd)/PORT"

lnfix_of_rom() {

    #1 Modifies line from build.prop of mi_ext
    sed -i 's/^ro.product.mod_device=.*/ro.product.mod_device=munch/' "$PORT_dir/mi_ext/etc/build.prop"

    #2 Copies all line from build.prop of mi_ext
    sed -n '1,20p' "$PORT_dir/mi_ext/etc/build.prop" >> "$PORT_dir/product/etc/build.prop"

    #3 Delete vk key from build.prop of product
    sed -i '/vk/d' "$PORT_dir/product/etc/build.prop"

    #4 Modify codename to munch
    sed -i 's/^\(ro.product.product.name=miproduct_\).*/\1munch/' "$PORT_dir/product/etc/build.prop"

    #5 Modify fingerprint to munch
    sed -i 's#^\(ro.product.build.fingerprint=Xiaomi/\)[^/]\+#\1munch#' "$PORT_dir/product/etc/build.prop"

    #6 Modify density
    sed -i 's/^\(persist\.miui\.density_v2=\).*/\1440/' "$PORT_dir/product/etc/build.prop"
    sed -i 's/^\(ro\.sf\.lcd_density=\).*/\1440/' "$PORT_dir/product/etc/build.prop"
}

lnfix_of_rom