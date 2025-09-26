#!/bin/bash

read -rp "Provide the PORT directory name: " prov_dir

port_dir="/data/DNA/$prov_dir"

lnfix_of_rom() {

    #1 Modifies line from build.prop of mi_ext
    sed -i 's/^ro.product.mod_device=.*/ro.product.mod_device=munch/' "$port_dir/mi_ext/etc/build.prop"

    #2 Copies all line from build.prop of mi_ext
    sed -n '1,20p' "$port_dir/mi_ext/etc/build.prop" >> "$port_dir/product/etc/build.prop"

    #3 Delete key from build.prop of product
    sed -i '/^persist.sys.enhance_vkpipelinecache.enable=/d' "$port_dir/product/etc/build.prop"

    #4 Modify codename to munch
    sed -i 's/^\(ro.product.product.name=miproduct_\).*/\1munch/' "$port_dir/product/etc/build.prop"

    #5 Modify fingerprint to munch
    sed -i 's#^\(ro.product.build.fingerprint=Xiaomi/\)[^/]\+#\1munch#' "$port_dir/product/etc/build.prop"

    #6 Modify density
    sed -i 's/^\(persist\.miui\.density_v2=\).*/\1440/' "$port_dir/product/etc/build.prop"
    sed -i 's/^\(ro\.sf\.lcd_density=\).*/\1440/' "$port_dir/product/etc/build.prop"
}

lnfix_of_rom