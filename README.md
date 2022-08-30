## ELF LAYOUT MAP VIEW
根据map_view.cfg中的sections来生成一张结构图, 展示segment对section的包含关系.

最初目的是为了帮助理解和学习ELF格式.

**输出范例：**
```
{ [0x0h]elf(.so)
  { [0x0h]PT_LOAD(0)
    { [0x0h]ehdr
    } [0x33h]ehdr

    { [0x34h]PT_PHDR / phdr
    } [0x133h]PT_PHDR / phdr

    { [0x134h].interp / PT_INERP
    } [0x146h].interp / PT_INERP

    /* gap size: 1h  */
    { [0x148h].dynsym / DT_SYMTAB
    } [0x607h].dynsym / DT_SYMTAB

    { [0x608h].dynstr / DT_STRTAB
    } [0xbdah].dynstr / DT_STRTAB

    /* gap size: 1h  */
    { [0xbdch].hash / DT_HASH
    } [0xe1fh].hash / DT_HASH

    { [0xe20h].rel.dyn / DT_REL
    } [0xe67h].rel.dyn / DT_REL

    { [0xe68h].rel.plt / DT_JMPREL
    } [0xf1fh].rel.plt / DT_JMPREL

    { [0xf20h].plt
    } [0x1047h].plt

    { [0x1048h].text
    } [0x2b23h].text

    { [0x2b24h].ARM.extab
    } [0x2b8fh].ARM.extab

    { [0x2b90h].ARM.exidx
    } [0x2cbfh].ARM.exidx

    { [0x2cc0h].rodata
    } [0x2d2fh].rodata
  } [0x2d2fh]PT_LOAD(0)

  /* gap size: 113ch  */
  { [0x3e6ch]PT_LOAD(1)
    { [0x3e6ch]PT_UNK_70000001h
      { [0x3e6ch].fini_array / DT_FINI_ARRAY
      } [0x3e73h].fini_array / DT_FINI_ARRAY

      { [0x3e74h].init_array / DT_INIT_ARRAY
      } [0x3e77h].init_array / DT_INIT_ARRAY

      { [0x3e78h].dynamic / PT_DYNAMIC
      } [0x3f77h].dynamic / PT_DYNAMIC

      { [0x3f78h].got
        { [0x3f98h]DT_PLTGOT
        } [0x3fffh]DT_PLTGOT
      } [0x3fffh].got
    } [0x3fffh]PT_UNK_70000001h

    { [0x4000h].data
    } [0x4003h].data
  } [0x4003h]PT_LOAD(1)
} [0x4003h]elf(.so)
```

