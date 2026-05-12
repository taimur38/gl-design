-- growthlabbify.lua
--
-- Pandoc Lua filter for Growth Lab report formatting.
--
-- Features:
--   1. Figure titles placed above images with "Figure Title" style
--   2. Consecutive images (2–3) rendered side-by-side, snapped to grid
--   3. "Source:" paragraphs after figures styled as "Figure Source"
--   4. Title + image + source kept together via keepNext styles
--   5. Fenced-div boxes → GL-styled callout (brand-blue left border)
--   6. Citeproc bibliography gets a "References" H1 heading
--
-- Grid reference (recipes/report.md):
--   Live width: 6.5"  (US Letter, 1" margins)
--   6 columns × 0.944" + 5 gutters × 0.167"
--   Full (6 col) = 6.500"   Half (3 col) = 3.167"
--   Major (4 col) = 4.278"  Minor (2 col) = 2.056"

--------------------------------------------------------------------------------
-- GL design tokens
--------------------------------------------------------------------------------

local GL = {
  content_width = 6.5,       -- inches (live area)
  col_width     = 0.944,     -- single column width
  gutter        = 0.167,     -- gutter between columns

  -- Named grid spans (inches)
  span_full     = 6.500,     -- 6 columns
  span_major    = 4.278,     -- 4 columns
  span_half     = 3.167,     -- 3 columns
  span_minor    = 2.056,     -- 2 columns

  -- Colors
  brand_blue    = "266798",
  text_dark     = "333333",
  text_muted    = "7c7c7c",
  border        = "DCDCDC",
  background    = "F3F3F3",

  -- Fonts
  font_sans     = "Source Sans 3",
  font_mono     = "JetBrains Mono",
}

-- DXA conversions (1 inch = 1440 DXA, 1pt = 20 DXA)
local CONTENT_WIDTH_DXA = math.floor(GL.content_width * 1440)  -- 9360

--------------------------------------------------------------------------------
-- XML helpers for raw OpenXML output
--------------------------------------------------------------------------------

local function esc(s)
  return s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
end

-- Convert pandoc inlines to OpenXML w:r elements.
-- `rpr` accumulates nested run properties (bold, italic, etc.)
local function inlines_to_ooxml(inlines, rpr)
  rpr = rpr or ""
  local buf = {}
  for _, il in ipairs(inlines) do
    if il.t == "Str" then
      local rpr_xml = rpr ~= "" and ("<w:rPr>" .. rpr .. "</w:rPr>") or ""
      buf[#buf+1] = "<w:r>" .. rpr_xml
        .. '<w:t xml:space="preserve">' .. esc(il.text) .. "</w:t></w:r>"
    elseif il.t == "Space" or il.t == "SoftBreak" then
      buf[#buf+1] = '<w:r><w:t xml:space="preserve"> </w:t></w:r>'
    elseif il.t == "LineBreak" then
      buf[#buf+1] = "<w:r><w:br/></w:r>"
    elseif il.t == "Strong" then
      buf[#buf+1] = inlines_to_ooxml(il.content, rpr .. "<w:b/><w:bCs/>")
    elseif il.t == "Emph" then
      buf[#buf+1] = inlines_to_ooxml(il.content, rpr .. "<w:i/><w:iCs/>")
    elseif il.t == "Code" then
      local code_rpr = rpr
        .. '<w:rFonts w:ascii="' .. GL.font_mono .. '" w:hAnsi="' .. GL.font_mono .. '"/>'
        .. '<w:sz w:val="20"/><w:szCs w:val="20"/>'  -- 10pt for inline code
      buf[#buf+1] = "<w:r><w:rPr>" .. code_rpr .. "</w:rPr>"
        .. '<w:t xml:space="preserve">' .. esc(il.text) .. "</w:t></w:r>"
    elseif il.t == "Superscript" then
      buf[#buf+1] = inlines_to_ooxml(il.content, rpr .. '<w:vertAlign w:val="superscript"/>')
    elseif il.t == "Subscript" then
      buf[#buf+1] = inlines_to_ooxml(il.content, rpr .. '<w:vertAlign w:val="subscript"/>')
    end
  end
  return table.concat(buf)
end

-- Convert a single pandoc Block to OpenXML paragraph(s)
local function block_to_ooxml(block)
  if block.t == "Para" or block.t == "Plain" then
    return "<w:p>" .. inlines_to_ooxml(block.content) .. "</w:p>"
  elseif block.t == "BulletList" then
    local buf = {}
    for _, item in ipairs(block.content) do
      for _, b in ipairs(item) do
        if b.t == "Para" or b.t == "Plain" then
          buf[#buf+1] = '<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>'
            .. inlines_to_ooxml(b.content) .. "</w:p>"
        end
      end
    end
    return table.concat(buf)
  elseif block.t == "OrderedList" then
    local buf = {}
    for _, item in ipairs(block.content) do
      for _, b in ipairs(item) do
        if b.t == "Para" or b.t == "Plain" then
          buf[#buf+1] = '<w:p><w:pPr><w:pStyle w:val="ListNumber"/></w:pPr>'
            .. inlines_to_ooxml(b.content) .. "</w:p>"
        end
      end
    end
    return table.concat(buf)
  elseif block.t == "BlockQuote" then
    local buf = {}
    for _, b in ipairs(block.content) do
      buf[#buf+1] = block_to_ooxml(b)
    end
    return table.concat(buf)
  end
  return ""
end

--------------------------------------------------------------------------------
-- Box builder — GL call-out style
--
-- Visual spec (recipes/report.md § 5, "Pull quotes / call-out boxes"):
--   Background: #F3F3F3
--   Left border: 3pt solid #266798 (brand blue)
--   Other borders: none (clean left-accent style)
--   Padding: 12pt all sides
--   Title: Source Sans 3 SemiBold in brand blue
--------------------------------------------------------------------------------

local function make_box(title, blocks)
  local pad = 173  -- 12pt in DXA (12 × 14.4 ≈ 173)
  local buf = {}

  buf[#buf+1] = "<w:tbl>"
  buf[#buf+1] = "<w:tblPr>"
  buf[#buf+1] = '<w:tblW w:w="5000" w:type="pct"/>'
  -- Left-accent border: heavy brand-blue left, no other borders
  buf[#buf+1] = "<w:tblBorders>"
  buf[#buf+1] = '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
  buf[#buf+1] = '<w:left w:val="single" w:sz="24" w:space="0" w:color="' .. GL.brand_blue .. '"/>'
  buf[#buf+1] = '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
  buf[#buf+1] = '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
  buf[#buf+1] = "</w:tblBorders>"
  buf[#buf+1] = "<w:tblCellMar>"
  buf[#buf+1] = '<w:top w:w="' .. pad .. '" w:type="dxa"/>'
  buf[#buf+1] = '<w:left w:w="' .. (pad + 60) .. '" w:type="dxa"/>'  -- extra left for border breathing
  buf[#buf+1] = '<w:bottom w:w="' .. pad .. '" w:type="dxa"/>'
  buf[#buf+1] = '<w:right w:w="' .. pad .. '" w:type="dxa"/>'
  buf[#buf+1] = "</w:tblCellMar>"
  buf[#buf+1] = "</w:tblPr>"
  buf[#buf+1] = '<w:tblGrid><w:gridCol w:w="' .. CONTENT_WIDTH_DXA .. '"/></w:tblGrid>'
  buf[#buf+1] = "<w:tr><w:tc>"
  buf[#buf+1] = '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="' .. GL.background .. '"/></w:tcPr>'

  -- Title paragraph: brand blue, semibold, Source Sans 3
  if title then
    buf[#buf+1] = '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr>'
      .. '<w:r><w:rPr>'
      .. '<w:rFonts w:ascii="' .. GL.font_sans .. '" w:hAnsi="' .. GL.font_sans .. '"/>'
      .. '<w:b/><w:bCs/>'
      .. '<w:color w:val="' .. GL.brand_blue .. '"/>'
      .. '</w:rPr>'
      .. '<w:t xml:space="preserve">' .. esc(title) .. "</w:t></w:r></w:p>"
  end

  -- Content blocks
  for _, block in ipairs(blocks) do
    local xml = block_to_ooxml(block)
    if xml ~= "" then buf[#buf+1] = xml end
  end

  buf[#buf+1] = "</w:tc></w:tr></w:tbl>"
  return pandoc.RawBlock("openxml", table.concat(buf, "\n"))
end

--------------------------------------------------------------------------------
-- Figure helpers
--------------------------------------------------------------------------------

local function is_figure(block)
  return block.t == "Figure"
end

-- A paragraph that contains only images (and whitespace)
local function is_image_para(block)
  if block.t ~= "Para" and block.t ~= "Plain" then return false end
  local has_image = false
  for _, il in ipairs(block.content) do
    if il.t == "Image" then
      has_image = true
    elseif il.t ~= "Space" and il.t ~= "SoftBreak" and il.t ~= "LineBreak" then
      return false
    end
  end
  return has_image
end

local function is_figure_block(block)
  return is_figure(block) or is_image_para(block)
end

local function is_source_para(block)
  if block.t ~= "Para" then return false end
  local text = pandoc.utils.stringify(block)
  return text:match("^%s*[Ss]ources?%s*:")
      or text:match("^%s*[Nn]otes?%s*:")
end

-- Extract caption inlines from a Figure element
local function get_caption_inlines(fig)
  if fig.t ~= "Figure" then return nil end
  local cap = fig.caption.long
  if not cap or #cap == 0 then return nil end
  local inlines = {}
  for _, block in ipairs(cap) do
    if block.t == "Para" or block.t == "Plain" then
      if #inlines > 0 then
        table.insert(inlines, pandoc.Space())
      end
      for _, il in ipairs(block.content) do
        table.insert(inlines, il)
      end
    end
  end
  if #inlines == 0 then return nil end
  return inlines
end

-- Extract all Image elements from a block
local function get_images(block)
  local images = {}
  local children
  if block.t == "Figure" then
    children = block.content
  elseif block.t == "Para" or block.t == "Plain" then
    children = {block}
  else
    return images
  end
  for _, b in ipairs(children) do
    if b.t == "Para" or b.t == "Plain" then
      for _, il in ipairs(b.content) do
        if il.t == "Image" then
          table.insert(images, il)
        end
      end
    end
  end
  return images
end

--------------------------------------------------------------------------------
-- Output builders
--------------------------------------------------------------------------------

local function styled_div(content, style_name)
  return pandoc.Div(content, pandoc.Attr("", {}, {{"custom-style", style_name}}))
end

local function make_title(inlines)
  return styled_div({pandoc.Para(inlines)}, "Figure Title")
end

local function make_source(para)
  return styled_div({para}, "Figure Source")
end

local function make_image_block(img)
  return styled_div({pandoc.Para({img})}, "Figure Image")
end

-- Place images side-by-side, snapped to the GL grid.
--
-- 2 images → each gets "half" width (3 cols = 3.167")
-- 3 images → each gets "minor" width (2 cols = 2.056")
--
-- The gutter between images is the grid gutter (0.167").
local function make_side_by_side(images)
  local n = #images
  local img_width
  if n == 2 then
    img_width = GL.span_half
  elseif n == 3 then
    img_width = GL.span_minor
  else
    img_width = (GL.content_width - (n - 1) * GL.gutter) / n
  end

  local width_str = string.format("%.2fin", img_width)
  local inlines = {}

  for i, img in ipairs(images) do
    local new_img = pandoc.Image(
      img.caption, img.src, img.title,
      pandoc.Attr(img.identifier, img.classes, {width = width_str})
    )
    if i > 1 then
      table.insert(inlines, pandoc.Space())
    end
    table.insert(inlines, new_img)
  end

  return styled_div({pandoc.Para(inlines)}, "Figure Image")
end

--------------------------------------------------------------------------------
-- Detect the citeproc refs div
local function is_refs_div(block)
  return block.t == "Div" and block.identifier == "refs"
end

--------------------------------------------------------------------------------
-- Horizontal rules → thin line in border color
--------------------------------------------------------------------------------

local function make_hr()
  local xml = '<w:p><w:pPr>'
    .. '<w:spacing w:before="173" w:after="173"/>'  -- 12pt above and below
    .. '<w:pBdr>'
    .. '<w:bottom w:val="single" w:sz="4" w:space="1" w:color="' .. GL.border .. '"/>'
    .. '</w:pBdr>'
    .. '</w:pPr></w:p>'
  return pandoc.RawBlock("openxml", xml)
end

--------------------------------------------------------------------------------
-- Main filter: walk blocks and group consecutive figures
--------------------------------------------------------------------------------

function Pandoc(doc)
  local blocks = doc.blocks
  local out = {}
  local i = 1

  while i <= #blocks do

    -- Horizontal rules → GL-styled thin line
    if blocks[i].t == "HorizontalRule" then
      table.insert(out, make_hr())
      i = i + 1

    -- Convert box divs to GL-styled callout tables
    elseif blocks[i].t == "Div" and blocks[i].classes:includes("box") then
      local div = blocks[i]
      local title = div.attributes["title"]
      table.insert(out, make_box(title, div.content))
      i = i + 1

    -- Insert a "References" heading before the citeproc bibliography div
    elseif is_refs_div(blocks[i]) then
      table.insert(out, pandoc.Header(1, pandoc.Str("References")))
      table.insert(out, blocks[i])
      i = i + 1

    elseif is_figure_block(blocks[i]) then
      -- Collect consecutive figure/image blocks
      local group = {blocks[i]}
      local j = i + 1
      while j <= #blocks and is_figure_block(blocks[j]) do
        table.insert(group, blocks[j])
        j = j + 1
      end

      -- Check for a "Source:" or "Note:" paragraph immediately after
      local source = nil
      if j <= #blocks and is_source_para(blocks[j]) then
        source = blocks[j]
        j = j + 1
      end

      -- Gather all images and captions from the group
      local all_images = {}
      local captions = {}
      for _, item in ipairs(group) do
        for _, img in ipairs(get_images(item)) do
          table.insert(all_images, img)
        end
        local cap = get_caption_inlines(item)
        if cap then table.insert(captions, cap) end
      end

      -- Emit: titles → images → source
      -- When side-by-side, merge captions: "Title one (left); Title two (right)"
      if #all_images >= 2 and #all_images <= 3 and #captions >= 2 then
        local labels = {"left", "center", "right"}
        if #captions == 2 then labels = {"left", "right"} end
        local merged = {}
        for ci, cap_inlines in ipairs(captions) do
          if ci > 1 then
            table.insert(merged, pandoc.Str(";"))
            table.insert(merged, pandoc.Space())
          end
          for _, il in ipairs(cap_inlines) do
            table.insert(merged, il)
          end
          table.insert(merged, pandoc.Space())
          table.insert(merged, pandoc.Str("(" .. labels[ci] .. ")"))
        end
        table.insert(out, make_title(merged))
      else
        for _, cap_inlines in ipairs(captions) do
          table.insert(out, make_title(cap_inlines))
        end
      end

      if #all_images >= 2 and #all_images <= 3 then
        table.insert(out, make_side_by_side(all_images))
      else
        for _, img in ipairs(all_images) do
          table.insert(out, make_image_block(img))
        end
      end

      if source then
        table.insert(out, make_source(source))
      end

      i = j
    else
      table.insert(out, blocks[i])
      i = i + 1
    end
  end

  doc.blocks = out
  return doc
end
